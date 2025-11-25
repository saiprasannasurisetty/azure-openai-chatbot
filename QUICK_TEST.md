# 🚀 QUICK REFERENCE - Remote Testing in 5 Minutes

## ⚡ Super Quick Start

```bash
# 1. GET YOUR PUBLIC URL
ngrok http 8080
# Copy: https://abc123-def456.ngrok.io

# 2. TEST IT WORKS
curl https://abc123-def456.ngrok.io/health

# 3. GENERATE API KEY
curl -X POST https://abc123-def456.ngrok.io/auth/generate-key
# Save the key!

# 4. SEND YOUR FIRST MESSAGE
curl -X POST https://abc123-def456.ngrok.io/chat \
  -H "Authorization: Bearer YOUR_KEY_HERE" \
  -H "X-Session-ID: test" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello! What can you do?"}'

# 5. VIEW CONVERSATION
curl https://abc123-def456.ngrok.io/history \
  -H "Authorization: Bearer YOUR_KEY_HERE" \
  -H "X-Session-ID: test"
```

---

## 💬 Best Questions to Ask

### Quick Wins (Always Work)
```
"Hello!"
"What is Python?"
"Tell me about Azure"
"What is artificial intelligence?"
"How does the internet work?"
"Explain machine learning"
"What is cloud computing?"
"Tell me about GitHub"
```

### Technical Deep Dives
```
"How do I deploy an app?"
"What is Docker?"
"Explain REST APIs"
"What is authentication?"
"How does rate limiting work?"
"Explain microservices"
"What is CI/CD?"
"Tell me about Git"
```

### For Your Chatbot Specifically
```
"What features do you have?"
"How do I use your API?"
"What is a session ID?"
"How does authentication work?"
"What's the rate limit?"
"Can you remember conversations?"
"How do I access the history?"
"What happens if I exceed the rate limit?"
```

### Fun/Conversational
```
"How are you?"
"Do you like chatbots?"
"What's your favorite programming language?"
"Can you tell me a joke?"
"What's the meaning of life?"
"What should I learn next?"
"Any recommendations for me?"
"What's the best way to learn coding?"
```

---

## 🔑 Key Endpoints

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/health` | GET | ❌ | Check if app is running |
| `/auth/generate-key` | POST | ❌ | Create API key |
| `/chat` | POST | ✅ | Send message |
| `/history` | GET | ✅ | Get conversation |

---

## 📝 Response Examples

### Health Check
```json
{
  "status": "ok",
  "local_mode": true,
  "azure_configured": false
}
```

### API Key Response
```json
{
  "api_key": "anYD5g55DgBt4xDrwi2yu3Q2bBDPaoVfxyVd039RJ88",
  "message": "Store this key securely...",
  "usage": "Authorization: Bearer <api_key>"
}
```

### Chat Response (LOCAL_MODE)
```json
{
  "from": "local",
  "session_id": "test",
  "response": "MOCK-ASSISTANT: I received your prompt (29 chars). Summary: Hello! What can you do?"
}
```

### History Response
```json
{
  "session_id": "test",
  "history": [
    {
      "role": "user",
      "content": "Hello! What can you do?",
      "timestamp": "2025-11-25T06:14:13"
    },
    {
      "role": "assistant",
      "content": "MOCK-ASSISTANT: I received your prompt...",
      "timestamp": "2025-11-25T06:14:13"
    }
  ],
  "total_messages": 2
}
```

---

## 🧪 Testing Checklist

- [ ] Ngrok running: `ngrok http 8080`
- [ ] Public URL copied
- [ ] Health check works: `/health` returns ok
- [ ] API key generated and saved
- [ ] First message sent successfully
- [ ] Response received and displayed
- [ ] History shows both user & bot messages
- [ ] Try multiple questions
- [ ] Different session IDs keep messages separate
- [ ] URL works from another device

---

## ❌ Common Issues & Fixes

| Problem | Fix |
|---------|-----|
| "Connection refused" | Is app running? Check: `python src/app.py` |
| "Invalid API key" | Generate new key, copy entire value |
| "Timeout" | Keep ngrok terminal open |
| "URL not working" | Ngrok might have restarted, get new URL |
| "401 Unauthorized" | Missing `Authorization: Bearer` header |
| "No messages showing" | Make sure session IDs match |

---

## 🎯 Headers You Need

For ALL authenticated requests (`/chat`, `/history`):

```
Authorization: Bearer YOUR_API_KEY
X-Session-ID: your-session-name
Content-Type: application/json
```

---

## 📱 Share with Others

Once testing works, share your URL:

```
Try my chatbot! 🤖
URL: https://abc123-def456.ngrok.io

Steps:
1. Get API key: POST /auth/generate-key
2. Send message: POST /chat with Bearer token
3. View history: GET /history

Try asking:
- "What is artificial intelligence?"
- "Tell me about Python"
- "Explain cloud computing"
```

---

## 🔗 Useful Links

- **Ngrok**: https://ngrok.com
- **Cloudflare Tunnel**: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/
- **Full Testing Guide**: `REMOTE_TESTING_GUIDE.md`
- **All Guides**: `START_HERE.md`

---

## ⏱️ What to Expect

| Scenario | Timing |
|----------|--------|
| Get public URL | 1 minute |
| Generate API key | 5 seconds |
| Send first message | 2 seconds |
| Get response | 1 second |
| View history | 1 second |
| **Total time** | **~2-3 minutes** |

---

**Ready?** Download Ngrok and start testing now! 🚀

