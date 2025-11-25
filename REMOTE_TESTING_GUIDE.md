# 🧪 Remote Testing Guide - Questions & Examples

Your chatbot is ready to test remotely! Here's everything you need to know.

---

## 🚀 Step 1: Get a Public URL (5 minutes)

### Option A: Ngrok (Easiest)
```powershell
# 1. Download from: https://ngrok.com/download
# 2. Extract and run:
cd C:\ngrok
.\ngrok http 8080

# 3. You'll see:
# Forwarding: https://abc123-def456.ngrok.io -> http://localhost:8080
```

### Option B: Cloudflare Tunnel (Better for long-term)
```powershell
# Download cloudflared from: https://github.com/cloudflare/cloudflared/releases
# Run:
cloudflared tunnel --url http://localhost:8080
```

**Keep terminal open!** Your public URL is active while the tunnel runs.

---

## ✅ Step 2: Test the Chatbot

### Health Check (No Auth Needed)
```bash
curl https://YOUR_URL/health

# Response:
# {"status": "ok", "local_mode": true, "azure_configured": false}
```

### Step 1: Generate API Key
```bash
curl -X POST https://YOUR_URL/auth/generate-key

# Response:
# {
#   "api_key": "anYD5g55DgBt4xDrwi2yu3Q2bBDPaoVfxyVd039RJ88",
#   "message": "Store this key securely...",
#   "usage": "Authorization: Bearer <api_key>"
# }
```

**SAVE THIS KEY!** You'll need it for all chat requests.

### Step 2: Send Your First Message
```bash
curl -X POST https://YOUR_URL/chat \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "X-Session-ID: session-1" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello! What can you do?"}'

# Response:
# {
#   "from": "local",
#   "session_id": "session-1",
#   "response": "MOCK-ASSISTANT: I received your prompt (29 chars). Summary: Hello! What can you do?"
# }
```

### Step 3: Continue the Conversation
```bash
# Send another message in SAME session
curl -X POST https://YOUR_URL/chat \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "X-Session-ID: session-1" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Tell me about Python"}'
```

### Step 4: Retrieve Conversation History
```bash
curl https://YOUR_URL/history \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "X-Session-ID: session-1"

# Response shows all messages in this session
```

---

## 💬 Sample Questions to Ask the Chatbot

### General Knowledge Questions
- "What is artificial intelligence?"
- "Explain machine learning in simple terms"
- "What is cloud computing?"
- "Tell me about Python programming"
- "What is Azure?"
- "Explain what REST APIs are"
- "What is Docker and why use it?"
- "Tell me about Git version control"
- "What is a database?"
- "Explain the difference between frontend and backend"

### Technical Questions
- "How do I install Python?"
- "What is the difference between HTTP and HTTPS?"
- "Explain JSON format"
- "What is API authentication?"
- "How does a web server work?"
- "What is a microservice?"
- "Tell me about containerization"
- "What is CI/CD?"
- "Explain rate limiting"
- "What is a webhook?"

### Azure Specific
- "What is Azure App Service?"
- "How do I deploy to Azure?"
- "What is Azure OpenAI?"
- "Tell me about Azure resources"
- "What is Azure Container Registry?"
- "How does Azure DevOps work?"

### Career & Learning
- "What skills should I learn for cloud development?"
- "What is the best way to learn programming?"
- "What's the difference between junior and senior developers?"
- "How do I become a cloud architect?"
- "What certifications are worth getting?"

### Fun Conversational
- "How are you?"
- "What's your name?"
- "Do you like chatbots?"
- "Tell me a joke"
- "What's the meaning of life?"
- "Can you help me with something?"

---

## 📊 Understanding the Responses

### In LOCAL_MODE (What You're Testing With)

**Response Format**:
```json
{
  "from": "local",
  "session_id": "session-1",
  "response": "MOCK-ASSISTANT: I received your prompt (XX chars). Summary: [your question summarized]"
}
```

**What This Means**:
- `"from": "local"` → Using mock responses (for testing)
- `session_id` → Your conversation thread
- `response` → The chatbot's reply
- Character count → Shows it processed your input
- Summary → Echo of what you asked

### When Using Real Azure OpenAI (After Quota Approval)

**Response Format**:
```json
{
  "from": "azure",
  "session_id": "session-1",
  "response": "Detailed response from OpenAI GPT model...",
  "result": {
    "choices": [...],
    "usage": {...}
  }
}
```

**What's Different**:
- `"from": "azure"` → Real OpenAI responses
- Much longer, more detailed responses
- Shows token usage
- Real AI-generated answers

---

## 🧪 Complete Testing Workflow

### PowerShell Script (Windows)
```powershell
# 1. Set your URL and API key
$URL = "https://abc123-def456.ngrok.io"  # Replace with your URL
$BODY_ENCODE = [System.Text.Encoding]::UTF8

# 2. Generate API key
$response = Invoke-WebRequest -Uri "$URL/auth/generate-key" -Method POST
$apiKey = ($response.Content | ConvertFrom-Json).api_key
Write-Host "API Key: $apiKey"

# 3. Send message
$headers = @{
    "Authorization" = "Bearer $apiKey"
    "X-Session-ID" = "test-session"
    "Content-Type" = "application/json"
}

$message = @{
    "prompt" = "Hello! What can you do?"
} | ConvertTo-Json

$chatResponse = Invoke-WebRequest -Uri "$URL/chat" -Method POST -Headers $headers -Body $message
Write-Host ($chatResponse.Content | ConvertFrom-Json | ConvertTo-Json)

# 4. Get history
$historyResponse = Invoke-WebRequest -Uri "$URL/history" -Method GET -Headers $headers
Write-Host ($historyResponse.Content | ConvertFrom-Json | ConvertTo-Json)
```

### Bash Script (macOS/Linux)
```bash
#!/bin/bash

URL="https://abc123-def456.ngrok.io"

# 1. Generate API key
echo "Generating API key..."
API_KEY=$(curl -s -X POST "$URL/auth/generate-key" | jq -r '.api_key')
echo "API Key: $API_KEY"

# 2. Send messages
echo -e "\n--- Message 1 ---"
curl -X POST "$URL/chat" \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Session-ID: session-1" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello! What can you do?"}' | jq

# 3. Send another message
echo -e "\n--- Message 2 ---"
curl -X POST "$URL/chat" \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Session-ID: session-1" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Tell me about Python"}' | jq

# 4. Get history
echo -e "\n--- Conversation History ---"
curl "$URL/history" \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Session-ID: session-1" | jq
```

---

## 🎯 Multi-Session Testing

### Test Multiple Users
```bash
# User 1 Session
curl -X POST https://YOUR_URL/chat \
  -H "Authorization: Bearer API_KEY" \
  -H "X-Session-ID: alice-session" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hi, I am Alice"}'

# User 2 Session (different history)
curl -X POST https://YOUR_URL/chat \
  -H "Authorization: Bearer API_KEY" \
  -H "X-Session-ID: bob-session" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hi, I am Bob"}'

# Check Alice's history
curl https://YOUR_URL/history \
  -H "Authorization: Bearer API_KEY" \
  -H "X-Session-ID: alice-session"

# Check Bob's history (completely separate)
curl https://YOUR_URL/history \
  -H "Authorization: Bearer API_KEY" \
  -H "X-Session-ID: bob-session"
```

---

## ⚡ Rate Limiting Test

### Verify Rate Limiting Works
```bash
# Send 101 requests to trigger rate limit
for i in {1..101}; do
  curl -X POST https://YOUR_URL/chat \
    -H "Authorization: Bearer API_KEY" \
    -H "X-Session-ID: rate-test" \
    -H "Content-Type: application/json" \
    -d "{\"prompt\": \"Message $i\"}"
  
  if [ $i -eq 101 ]; then
    echo "Request 101 will show rate limit error (quota exceeded)"
  fi
done
```

**Expected**: First 100 work, request 101+ returns rate limit error ✅

---

## 🔍 Testing Best Practices

### 1. Test Different Question Types
- ✅ Simple greetings
- ✅ Technical questions
- ✅ Long prompts
- ✅ Special characters
- ✅ Numbers and dates

### 2. Test Edge Cases
- Empty message: `"prompt": ""`
- Very long message: 5000+ characters
- Unicode/emojis: `"prompt": "Hello 👋"`
- SQL injection attempt: Check it's handled safely
- XSS attempt: Check it's handled safely

### 3. Test Session Management
- Create multiple sessions
- Verify conversations don't mix
- Check history is separate per session
- Verify session isolation works

### 4. Test Authentication
- Valid API key: Works ✅
- Invalid API key: Returns 401 ❌
- No API key: Returns 401 ❌
- Expired key: Regenerate and try

### 5. Test Rate Limiting
- Send 100 requests: All succeed ✅
- Send 101st request: Rate limit error ✅
- Wait an hour: Quota resets ✅

---

## 📱 Share Your Testing Results

Once you have the URL, share it like this:

```
🤖 My Chatbot is Live!
URL: https://abc123-def456.ngrok.io

Quick Test:
1. Health: https://abc123-def456.ngrok.io/health
2. Get API Key: POST https://abc123-def456.ngrok.io/auth/generate-key
3. Chat: Send prompt to /chat endpoint with Bearer token

Questions to try:
- "Hello, what can you do?"
- "Tell me about Azure"
- "Explain machine learning"
```

---

## 🛠️ Common Testing Tools

### For Windows
```powershell
# Using PowerShell (built-in, what we used above)
# Using curl (if installed)
# Using Postman: https://www.postman.com/

# Install curl if needed:
# choco install curl
```

### For macOS/Linux
```bash
# curl (built-in)
# jq (install: brew install jq)
# Postman
# HTTPie: pip install httpie
```

### Using Postman (GUI Method)
1. Download: https://www.postman.com/
2. Create new request
3. POST to: `https://YOUR_URL/chat`
4. Headers:
   - `Authorization: Bearer YOUR_API_KEY`
   - `X-Session-ID: session-1`
   - `Content-Type: application/json`
5. Body (JSON): `{"prompt": "Your question here"}`
6. Click Send

---

## 📊 Sample Conversation

```
You: "Hello! What can you do?"
Bot: "MOCK-ASSISTANT: I received your prompt (29 chars). Summary: Hello! What can you do?"

You: "Tell me about Python"
Bot: "MOCK-ASSISTANT: I received your prompt (21 chars). Summary: Tell me about Python"

You: "What is a function?"
Bot: "MOCK-ASSISTANT: I received your prompt (20 chars). Summary: What is a function?"

---

When using Real Azure OpenAI (after quota approved):

You: "Hello! What can you do?"
Bot: "I'm an AI assistant that can help you with a wide variety of tasks. I can answer questions, help with writing, coding, math, creative projects, and much more. How can I help you today?"

You: "Tell me about Python"
Bot: "Python is a versatile, high-level programming language known for its simplicity and readability. It's widely used in web development, data science, artificial intelligence, automation, and more. Created by Guido van Rossum in 1991..."
```

---

## ✅ Testing Checklist

- [ ] Ngrok/Cloudflare tunnel running
- [ ] Public URL accessible
- [ ] Health endpoint works: `/health`
- [ ] Generate API key: `/auth/generate-key`
- [ ] Send message: `/chat` with valid key
- [ ] Retrieve history: `/history` with session
- [ ] Multiple sessions work independently
- [ ] Rate limiting works (100 req/hour)
- [ ] Can share URL with others
- [ ] Questions get responses

---

## 🎯 What to Look For in Responses

### Good Signs ✅
- Response received instantly
- Message shows in history
- Session ID persists
- API key validates
- Character count shown
- Summary includes keywords from your question

### Issues ❌
- 401 Unauthorized: Invalid API key
- 429 Too Many Requests: Rate limit exceeded
- 400 Bad Request: Invalid JSON format
- 500 Server Error: Something broke
- Timeout: App not responding

---

## 🚀 Next Steps

1. **Setup your public URL** (Ngrok or Cloudflare)
2. **Test the endpoints** (start with health check)
3. **Generate API key** (save it!)
4. **Send test messages** (try the questions above)
5. **Check the history** (verify persistence)
6. **Share the URL** (get feedback from others)
7. **After quota approval**: Deploy to Azure production

---

## 💡 Pro Tips

1. **Save your API key**: Don't regenerate every time
2. **Use same session ID**: For continuing conversations
3. **Test before sharing**: Make sure it's working
4. **Monitor responses**: Check LOCAL_MODE vs AZURE_MODE
5. **Keep ngrok running**: Terminal stays open
6. **Try different questions**: See how it handles variety
7. **Test with others**: Get real feedback

---

**Ready to test?** Start with your public URL and send your first message! 🚀

