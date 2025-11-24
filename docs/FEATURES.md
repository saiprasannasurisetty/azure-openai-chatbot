# Azure OpenAI Chatbot - Enhanced Features

## Overview
Your chatbot now includes **three major enterprise-grade features**:
1. **Message Persistence** - Store conversations in SQLite database
2. **API Authentication** - Secure endpoints with API keys
3. **Rate Limiting** - Prevent abuse with request throttling

---

## Features

### 1. Message Persistence (SQLite Database)
All conversations are persisted in a local SQLite database (`chatbot_data.db`).

**Benefits:**
- Conversations survive server restarts
- Query conversation history across sessions
- Track user interactions over time

**Endpoint:** `/history`
```bash
curl -X GET http://127.0.0.1:8080/history \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "X-Session-ID: user-123"
```

**Response:**
```json
{
  "session_id": "user-123",
  "history": [
    {
      "role": "user",
      "content": "What is Python?",
      "timestamp": "2025-11-24T15:30:45.123456"
    },
    {
      "role": "assistant",
      "content": "MOCK-ASSISTANT: ...",
      "timestamp": "2025-11-24T15:30:45.234567"
    }
  ],
  "total_messages": 2
}
```

---

### 2. API Authentication
All protected endpoints require API key authentication via Bearer token.

**Generate API Key:**
```bash
curl -X POST http://127.0.0.1:8080/auth/generate-key
```

**Response:**
```json
{
  "api_key": "anYD5g55DgBt4xDrwi2yu3Q2bBDPaoVfxyVd039RJ88",
  "message": "Store this key securely. Use it in Authorization header.",
  "usage": "Authorization: Bearer <api_key>"
}
```

**Use API Key:**
```bash
curl -X POST http://127.0.0.1:8080/chat \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "X-Session-ID: session-001" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Your question here"}'
```

**Public Endpoints (No Auth Required):**
- `GET /health` - Check app status

---

### 3. Rate Limiting
Prevents API abuse with configurable limits.

**Configuration:**
- **Limit:** 100 requests per hour (per API key)
- **Window:** 3600 seconds (1 hour)

**Rate Limit Exceeded Response (429):**
```json
{
  "error": "Rate limit exceeded",
  "details": "Max 100 requests per 3600 seconds"
}
```

**To modify limits**, edit `app.py`:
```python
RATE_LIMIT_REQUESTS = 100  # Change this
RATE_LIMIT_WINDOW = 3600   # Or this
```

---

## Database Schema

### Conversations Table
```sql
CREATE TABLE conversations (
  id INTEGER PRIMARY KEY,
  session_id TEXT UNIQUE NOT NULL,
  user_id TEXT,
  created_at TIMESTAMP
)
```

### Messages Table
```sql
CREATE TABLE messages (
  id INTEGER PRIMARY KEY,
  session_id TEXT NOT NULL,
  role TEXT NOT NULL,          -- 'user' or 'assistant'
  content TEXT NOT NULL,
  timestamp TIMESTAMP,
  FOREIGN KEY(session_id) REFERENCES conversations(session_id)
)
```

### Users Table
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  api_key TEXT UNIQUE NOT NULL,  -- SHA256 hashed
  created_at TIMESTAMP,
  active INTEGER                 -- 0 or 1
)
```

---

## Configuration

### Environment Variables

**Required:**
- `AZURE_OPENAI_ENDPOINT` - Your Azure OpenAI endpoint
- `AZURE_OPENAI_KEY` - Your Azure OpenAI API key
- `AZURE_OPENAI_DEPLOYMENT` - Your deployment name
- `LOCAL_MODE` - Set to "true" for mock responses

**Optional:**
- `API_KEY_SALT` - Salt for hashing API keys (default: "default-salt-change-in-production")
- `PORT` - Server port (default: 8080)

---

## API Endpoints Summary

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| GET | `/health` | No | Check app status |
| POST | `/auth/generate-key` | No | Generate new API key |
| POST | `/chat` | Yes | Send message & get response |
| GET | `/history` | Yes | Get conversation history |

---

## Usage Examples

### Example 1: Complete Workflow
```bash
# 1. Generate API key
API_KEY=$(curl -s -X POST http://127.0.0.1:8080/auth/generate-key | jq -r '.api_key')

# 2. Send a message
curl -X POST http://127.0.0.1:8080/chat \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Session-ID: user-100" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Hello, how are you?"}'

# 3. Get conversation history
curl -X GET http://127.0.0.1:8080/history \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Session-ID: user-100"
```

### Example 2: Multiple Sessions
```bash
# Session 1
curl -X POST http://127.0.0.1:8080/chat \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Session-ID: alice" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"I am Alice"}'

# Session 2
curl -X POST http://127.0.0.1:8080/chat \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Session-ID: bob" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"I am Bob"}'

# Both sessions maintain separate histories
```

---

## Security Notes

1. **API Keys**: Hashed using SHA256 before storage
2. **Key Storage**: Never share API keys; treat them like passwords
3. **Salt**: Change `API_KEY_SALT` in production
4. **HTTPS**: Use HTTPS in production (not just HTTP)
5. **Database**: Keep `chatbot_data.db` secure

---

## Troubleshooting

**Q: "Invalid API key" error?**
- Ensure you're using the correct API key
- Keys are case-sensitive
- Use the full key (don't truncate)

**Q: "Rate limit exceeded"?**
- Wait for the 1-hour window to reset
- Or reduce request frequency
- Generate a new API key if needed

**Q: Messages not persisting?**
- Check that `chatbot_data.db` exists and is writable
- Verify SQLite is installed
- Check application logs for database errors

**Q: Missing Authorization header?**
- Must include `Authorization: Bearer <api_key>` header
- Header is case-sensitive
- Don't use `/health` or `/auth/generate-key` as test endpoints for auth

---

## Next Steps

Consider adding:
- User management dashboard
- Analytics and usage metrics
- Message expiration/cleanup policies
- Backup and restore functionality
- Load balancing support
- WebSocket support for real-time chat
