# 🤖 Azure OpenAI Chatbot

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-green?style=flat&logo=flask)](https://flask.palletsprojects.com/)
[![Azure](https://img.shields.io/badge/Azure-OpenAI-0078D4?style=flat&logo=microsoft-azure)](https://azure.microsoft.com/en-us/products/ai-services/openai-service/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=flat)]()

A production-ready conversational AI chatbot powered by **Azure OpenAI**, featuring persistent message storage, API authentication, and rate limiting.

## ✨ Features

- 🔐 **Secure API Authentication** - Bearer token-based access control with hashed API keys
- 💾 **Message Persistence** - SQLite database stores conversations across sessions
- ⏱️ **Rate Limiting** - 100 requests/hour per API key to prevent abuse
- 📊 **Session Management** - Track multiple conversations independently
- ✅ **Input Validation** - Comprehensive prompt validation and error handling
- 🔄 **Local Fallback Mode** - Test without Azure credentials using mock responses
- 🚀 **Production Ready** - Error handling, logging, and security best practices

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Setup Instructions](#-setup-instructions)
- [API Documentation](#-api-documentation)
- [Usage Examples](#-usage-examples)
- [Configuration](#-configuration)
- [Database Schema](#-database-schema)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Azure OpenAI subscription (or use `LOCAL_MODE=true` for testing)
- pip/conda package manager

### 30-Second Setup

```bash
# 1. Clone the repository
git clone https://github.com/saiprasannasurisetty/azure-openai-chatbot.git
cd azure-openai-chatbot

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r config/requirements.txt

# 4. Configure environment
cp config/.env.example config/.env
# Edit config/.env with your Azure credentials or set LOCAL_MODE=true

# 5. Run the application
python src/app.py

# 6. Generate API key
curl -X POST http://127.0.0.1:8080/auth/generate-key

# 7. Send a message
curl -X POST http://127.0.0.1:8080/chat \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "X-Session-ID: session-1" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"What is AI?"}'
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Client Applications                   │
│              (Web, Mobile, CLI, Scripts)                │
└──────────────────┬──────────────────────────────────────┘
                   │
        ┌──────────▼──────────┐
        │   Flask API Server  │
        │   (Port 8080)       │
        └──────────┬──────────┘
                   │
        ┌──────────┴──────────────────────┐
        │                                 │
   ┌────▼─────┐              ┌──────────▼──────┐
   │ Auth Layer│              │ Request Handler │
   │ (Bearer)  │              │ & Validation    │
   └────┬─────┘              └──────────┬──────┘
        │                               │
   ┌────▼───────────┐         ┌────────▼────────┐
   │ Rate Limiting  │         │  Message Router │
   │ (100 req/hr)   │         │                 │
   └────┬───────────┘         └────────┬────────┘
        │                               │
        └───────────────┬───────────────┘
                        │
              ┌─────────▼─────────┐
              │   Decision Layer  │
              │ (Azure vs Local)  │
              └─────────┬─────────┘
                        │
            ┌───────────┴───────────┐
            │                       │
    ┌───────▼────────┐    ┌────────▼──────────┐
    │ Azure OpenAI   │    │ Local Mock Mode   │
    │ API Call       │    │ (Testing)         │
    └───────┬────────┘    └────────┬──────────┘
            │                       │
            └───────────┬───────────┘
                        │
              ┌─────────▼──────────┐
              │ SQLite Database    │
              │ (Persistence)      │
              │ - conversations    │
              │ - messages         │
              │ - users/api_keys   │
              └────────────────────┘
```

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | Python 3.8+ | Core application logic |
| **Framework** | Flask 2.0+ | HTTP API server |
| **AI Service** | Azure OpenAI | LLM-powered responses |
| **Database** | SQLite 3 | Message persistence |
| **Authentication** | SHA256 Hashing | Secure API keys |
| **Config** | python-dotenv | Environment management |
| **HTTP Client** | Requests | Azure API communication |

## 📦 Setup Instructions

### 1. Environment Setup

```bash
# Clone repository
git clone https://github.com/saiprasannasurisetty/azure-openai-chatbot.git
cd azure-openai-chatbot

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the `config/` directory:

```bash
cp config/.env.example config/.env
```

Edit `config/.env`:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT=your-deployment-name

# Application Settings
LOCAL_MODE=false          # Set to 'true' to use mock responses
PORT=8080                 # Server port
API_KEY_SALT=your-secret-salt  # Change this in production!
```

**For Testing:** Set `LOCAL_MODE=true` to use mock responses without Azure credentials.

### 3. Run Application

```bash
python src/app.py
```

Server will start on `http://127.0.0.1:8080`

### 4. Verify Installation

```bash
# Check health endpoint
curl http://127.0.0.1:8080/health

# Expected response:
# {"status": "ok", "local_mode": true, "azure_configured": false}
```

## 📡 API Documentation

### Authentication

All protected endpoints require an API key. Get one with:

```bash
curl -X POST http://127.0.0.1:8080/auth/generate-key
```

Response:
```json
{
  "api_key": "your-secure-api-key-here",
  "message": "Store this key securely. Use it in Authorization header.",
  "usage": "Authorization: Bearer <api_key>"
}
```

### Endpoints

#### 1. Health Check
```http
GET /health
```
**No authentication required**

Response:
```json
{
  "status": "ok",
  "local_mode": true,
  "azure_configured": true
}
```

#### 2. Generate API Key
```http
POST /auth/generate-key
```
**No authentication required**

Response:
```json
{
  "api_key": "anYD5g55DgBt4xDrwi2yu3Q2bBDPaoVfxyVd039RJ88",
  "message": "Store this key securely. Use it in Authorization header.",
  "usage": "Authorization: Bearer <api_key>"
}
```

#### 3. Send Message
```http
POST /chat
```
**Authentication required**

Headers:
```
Authorization: Bearer YOUR_API_KEY
X-Session-ID: session-identifier
Content-Type: application/json
```

Request Body:
```json
{
  "prompt": "What is machine learning?"
}
```

Response (Local Mode):
```json
{
  "from": "local",
  "session_id": "session-1",
  "response": "MOCK-ASSISTANT: I received your prompt (27 chars). Summary: What is machine learning?"
}
```

Response (Azure Mode):
```json
{
  "from": "azure",
  "session_id": "session-1",
  "response": "Machine learning is...",
  "result": { "choices": [...], "usage": {...} }
}
```

#### 4. Get Conversation History
```http
GET /history
```
**Authentication required**

Headers:
```
Authorization: Bearer YOUR_API_KEY
X-Session-ID: session-identifier
```

Response:
```json
{
  "session_id": "session-1",
  "history": [
    {
      "role": "user",
      "content": "What is Python?",
      "timestamp": "2025-11-24T15:30:45.123456"
    },
    {
      "role": "assistant",
      "content": "MOCK-ASSISTANT: I received your prompt...",
      "timestamp": "2025-11-24T15:30:45.234567"
    }
  ],
  "total_messages": 2
}
```

## 💡 Usage Examples

### Example 1: Complete Workflow

```bash
#!/bin/bash

# Generate API key
API_KEY=$(curl -s -X POST http://127.0.0.1:8080/auth/generate-key | jq -r '.api_key')
echo "API Key: $API_KEY"

# Send first message
curl -X POST http://127.0.0.1:8080/chat \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Session-ID: user-alice" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Hello, how are you?"}'

# Send second message (same session)
curl -X POST http://127.0.0.1:8080/chat \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Session-ID: user-alice" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Tell me about AI"}'

# Retrieve full conversation
curl -X GET http://127.0.0.1:8080/history \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Session-ID: user-alice"
```

### Example 2: Python Client

```python
import requests
import json

BASE_URL = "http://127.0.0.1:8080"

# Generate API key
key_response = requests.post(f"{BASE_URL}/auth/generate-key")
api_key = key_response.json()["api_key"]

headers = {
    "Authorization": f"Bearer {api_key}",
    "X-Session-ID": "python-session",
    "Content-Type": "application/json"
}

# Send message
response = requests.post(
    f"{BASE_URL}/chat",
    headers=headers,
    json={"prompt": "Explain quantum computing"}
)
print(response.json())

# Get history
history = requests.get(
    f"{BASE_URL}/history",
    headers=headers
)
print(history.json())
```

### Example 3: PowerShell (Included)

```powershell
# Run the test script
.\test_api.ps1
```

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AZURE_OPENAI_ENDPOINT` | - | Azure OpenAI API endpoint |
| `AZURE_OPENAI_KEY` | - | Azure OpenAI API key |
| `AZURE_OPENAI_DEPLOYMENT` | - | Deployment name |
| `LOCAL_MODE` | false | Use mock responses |
| `PORT` | 8080 | Server port |
| `API_KEY_SALT` | default-salt-* | Salt for key hashing |

### Rate Limiting Configuration

Edit in `app.py`:
```python
RATE_LIMIT_REQUESTS = 100    # Max requests
RATE_LIMIT_WINDOW = 3600     # Per seconds (1 hour)
```

## 🗄️ Database Schema

### SQLite Database Structure

```sql
-- Conversations table
CREATE TABLE conversations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL UNIQUE,
  user_id TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Messages table
CREATE TABLE messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL,
  role TEXT NOT NULL,           -- 'user' or 'assistant'
  content TEXT NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(session_id) REFERENCES conversations(session_id)
);

-- Users table (API keys)
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  api_key TEXT NOT NULL UNIQUE, -- SHA256 hashed
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  active INTEGER DEFAULT 1
);
```

## 🚀 Deployment

### Docker

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
COPY .env .

EXPOSE 8080
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t azure-openai-chatbot .
docker run -p 8080:8080 --env-file .env azure-openai-chatbot
```

### Azure App Service

```bash
# Install Azure CLI
# Configure with:
az login
az webapp create --resource-group mygroup --plan myplan --name mychatbot
az webapp up --resource-group mygroup --name mychatbot
```

### Heroku

```bash
heroku create your-chatbot-name
git push heroku main
heroku config:set AZURE_OPENAI_ENDPOINT=...
```

## 📚 Additional Resources

- [QUICKSTART.md](QUICKSTART.md) - 5-minute quick reference
- [FEATURES.md](FEATURES.md) - Complete feature documentation
- [IMPLEMENTATION.md](IMPLEMENTATION.md) - Technical architecture details
- [test_api.ps1](test_api.ps1) - PowerShell test suite

## 🔄 Future Enhancements

- [ ] User management dashboard with key lifecycle management
- [ ] Analytics dashboard - Usage metrics and statistics
- [ ] WebSocket support - Real-time conversations
- [ ] Message search & filtering across sessions
- [ ] Conversation export (JSON, PDF, CSV)
- [ ] Multi-region support for global deployment
- [ ] GraphQL API alternative to REST
- [ ] Message formatting - Markdown, code highlighting
- [ ] Conversation templates and presets
- [ ] Cost tracking per API key
- [ ] Webhook notifications for messages
- [ ] Multi-language support
- [ ] Custom system prompts per session
- [ ] Vector embeddings for semantic search
- [ ] Conversation branching and forking

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Sai Prasanna Surisetty**
- GitHub: [@saiprasannasurisetty](https://github.com/saiprasannasurisetty)
- Email: [contact info]

## 🙏 Acknowledgments

- Azure OpenAI team for the powerful AI service
- Flask community for the excellent web framework
- Contributors and users of this project

---

<div align="center">

**[⬆ back to top](#-azure-openai-chatbot)**

Made with ❤️ by Sai Prasanna

</div>
