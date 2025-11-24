# app.py — Flask app with Azure OpenAI, persistence, auth, and rate limiting
import os
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
import sqlite3
import hashlib
import secrets

load_dotenv()  # loads .env into environment if present

AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Warn if Azure credentials are not set and LOCAL_MODE is off
if not (os.getenv("LOCAL_MODE", "false").lower() in ("1", "true", "yes")):
    if not (AZURE_ENDPOINT and AZURE_KEY and AZURE_DEPLOYMENT):
        print("WARNING: Azure credentials not found. Set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, and AZURE_OPENAI_DEPLOYMENT environment variables, or set LOCAL_MODE=true to use mock mode.")

# If you want to force mock mode set LOCAL_MODE=true in .env or env vars
LOCAL_MODE = os.getenv("LOCAL_MODE", "false").lower() in ("1", "true", "yes")

# Configuration
DB_PATH = "chatbot_data.db"
API_KEY_SALT = os.getenv("API_KEY_SALT", "default-salt-change-in-production")
RATE_LIMIT_REQUESTS = 100  # requests per window
RATE_LIMIT_WINDOW = 3600   # 1 hour in seconds

app = Flask(__name__)

# In-memory rate limiting and authentication tracking
rate_limits = {}
active_tokens = {}

def init_database():
    """Initialize SQLite database for persistent storage"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Conversations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            user_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(session_id)
        )
    """)
    
    # Messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(session_id) REFERENCES conversations(session_id)
        )
    """)
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_key TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            active INTEGER DEFAULT 1
        )
    """)
    
    conn.commit()
    conn.close()

def hash_api_key(api_key):
    """Hash API key for storage"""
    return hashlib.sha256(f"{api_key}{API_KEY_SALT}".encode()).hexdigest()

def validate_api_key(api_key):
    """Validate API key from Authorization header"""
    if not api_key:
        return False
    
    # Check if key is in active tokens (cached)
    if api_key in active_tokens:
        if active_tokens[api_key] > datetime.now():
            return True
        else:
            del active_tokens[api_key]
    
    # Check database
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        hashed_key = hash_api_key(api_key)
        cursor.execute("SELECT id FROM users WHERE api_key = ? AND active = 1", (hashed_key,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            # Cache for 1 hour
            active_tokens[api_key] = datetime.now() + timedelta(hours=1)
            return True
    except Exception as e:
        print(f"API key validation error: {e}")
    
    return False

def check_rate_limit(identifier):
    """Check if request exceeds rate limit"""
    now = datetime.now()
    
    if identifier not in rate_limits:
        rate_limits[identifier] = []
    
    # Remove old requests outside the window
    rate_limits[identifier] = [
        req_time for req_time in rate_limits[identifier]
        if (now - req_time).total_seconds() < RATE_LIMIT_WINDOW
    ]
    
    if len(rate_limits[identifier]) >= RATE_LIMIT_REQUESTS:
        return False
    
    rate_limits[identifier].append(now)
    return True

def get_or_create_session(session_id, user_id=None):
    """Get or create a conversation session in database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR IGNORE INTO conversations (session_id, user_id)
            VALUES (?, ?)
        """, (session_id, user_id))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Session creation error: {e}")

def save_message(session_id, role, content):
    """Save message to database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO messages (session_id, role, content)
            VALUES (?, ?, ?)
        """, (session_id, role, content))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Message save error: {e}")

def get_persistent_history(session_id, limit=50):
    """Get conversation history from database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT role, content, timestamp FROM messages
            WHERE session_id = ?
            ORDER BY timestamp ASC
            LIMIT ?
        """, (session_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "role": row[0],
                "content": row[1],
                "timestamp": row[2]
            }
            for row in rows
        ]
    except Exception as e:
        print(f"History retrieval error: {e}")
        return []

def validate_prompt(prompt):
    """Validate and sanitize user input"""
    if not prompt or len(prompt.strip()) == 0:
        return None, "Prompt cannot be empty"
    if len(prompt) > 2000:
        return None, "Prompt too long (max 2000 characters)"
    return prompt.strip(), None

def get_session_id(request_obj):
    """Extract or generate session ID from request"""
    return request_obj.headers.get("X-Session-ID", "default")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "local_mode": LOCAL_MODE, "azure_configured": bool(AZURE_ENDPOINT and AZURE_KEY and AZURE_DEPLOYMENT)})

@app.route("/auth/generate-key", methods=["POST"])
def generate_api_key():
    """Generate a new API key for authentication"""
    try:
        new_key = secrets.token_urlsafe(32)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        hashed_key = hash_api_key(new_key)
        
        cursor.execute("INSERT INTO users (api_key) VALUES (?)", (hashed_key,))
        conn.commit()
        conn.close()
        
        return jsonify({
            "api_key": new_key,
            "message": "Store this key securely. Use it in Authorization header.",
            "usage": "Authorization: Bearer <api_key>"
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.before_request
def authenticate_request():
    """Authenticate requests using API key"""
    # Skip auth for health and key generation endpoints
    if request.path in ["/health", "/auth/generate-key"]:
        return
    
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401
    
    api_key = auth_header[7:]  # Remove "Bearer " prefix
    
    if not validate_api_key(api_key):
        return jsonify({"error": "Invalid API key"}), 401
    
    # Check rate limit
    if not check_rate_limit(api_key):
        return jsonify({
            "error": "Rate limit exceeded",
            "details": f"Max {RATE_LIMIT_REQUESTS} requests per {RATE_LIMIT_WINDOW} seconds"
        }), 429

@app.route("/history", methods=["GET"])
def get_chat_history():
    """Get persistent conversation history for a session"""
    session_id = get_session_id(request)
    history = get_persistent_history(session_id)
    return jsonify({
        "session_id": session_id,
        "history": history,
        "total_messages": len(history)
    })

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    user_prompt = data.get("prompt", "").strip()
    session_id = get_session_id(request)
    
    # Validate input
    validated_prompt, error = validate_prompt(user_prompt)
    if error:
        return jsonify({"error": error}), 400
    
    # Ensure session exists
    get_or_create_session(session_id)
    
    # Track user message
    save_message(session_id, "user", validated_prompt)

    # If Azure credentials exist and local mode not forced, use Azure
    if not LOCAL_MODE and AZURE_ENDPOINT and AZURE_KEY and AZURE_DEPLOYMENT:
        try:
            url = f"{AZURE_ENDPOINT}/openai/deployments/{AZURE_DEPLOYMENT}/completions?api-version=2023-06-01-preview"
            headers = {"api-key": AZURE_KEY, "Content-Type": "application/json"}
            body = {"prompt": validated_prompt, "max_tokens": 200}
            r = requests.post(url, json=body, headers=headers, timeout=15)
            r.raise_for_status()
            response_data = r.json()
            
            # Extract text from Azure response
            assistant_reply = response_data.get("choices", [{}])[0].get("text", "").strip()
            save_message(session_id, "assistant", assistant_reply)
            
            return jsonify({
                "from": "azure",
                "session_id": session_id,
                "response": assistant_reply,
                "result": response_data
            })
        except Exception as e:
            # If Azure call fails, return error but keep server alive
            return jsonify({"error": "azure_call_failed", "detail": str(e)}), 500

    # Local fallback/mock response when Azure not configured or LOCAL_MODE requested
    mock_reply = f"MOCK-ASSISTANT: I received your prompt ({len(validated_prompt)} chars). Summary: {validated_prompt[:140]}{'...' if len(validated_prompt) > 140 else ''}"
    save_message(session_id, "assistant", mock_reply)
    
    return jsonify({
        "from": "local",
        "session_id": session_id,
        "response": mock_reply
    })

if __name__ == "__main__":
    # Initialize database on startup
    init_database()
    print("Database initialized successfully")
    
    # default port 8080 (same as our README)
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)), debug=True)
