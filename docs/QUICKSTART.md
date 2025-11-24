# Quick Start Guide

## What's New?

Your Azure OpenAI chatbot now has **three enterprise features**:

1. **Persistent Message Storage** - Conversations saved to SQLite database
2. **API Key Authentication** - Secure all endpoints with Bearer token authentication
3. **Rate Limiting** - 100 requests/hour per API key

---

## Quick Start (5 minutes)

### Step 1: Generate API Key
```bash
curl -X POST http://127.0.0.1:8080/auth/generate-key
```

Save the returned `api_key` - you'll need it for all requests.

### Step 2: Send a Message
```bash
curl -X POST http://127.0.0.1:8080/chat \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "X-Session-ID: my-chat-1" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"What is AI?"}'
```

### Step 3: View Conversation History
```bash
curl -X GET http://127.0.0.1:8080/history \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "X-Session-ID: my-chat-1"
```

---

## Key Changes

### Before (Old App)
- ❌ No authentication
- ❌ Messages lost on restart
- ❌ No rate limiting
- ❌ No user tracking

### After (New App)
- ✅ API key authentication
- ✅ Persistent SQLite database
- ✅ Rate limiting (100 req/hour)
- ✅ Session-based tracking

---

## Important Headers

| Header | Purpose | Example |
|--------|---------|---------|
| `Authorization` | API authentication | `Bearer YOUR_API_KEY` |
| `X-Session-ID` | Track conversations | `session-abc-123` |
| `Content-Type` | Request format | `application/json` |

---

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| "Missing or invalid Authorization header" | No/wrong API key | Generate new key with `/auth/generate-key` |
| "Invalid API key" | Wrong key format | Copy entire key, no spaces |
| "Rate limit exceeded" | Too many requests | Wait 1 hour or generate new key |
| "Prompt cannot be empty" | Empty prompt | Provide non-empty "prompt" in JSON |

---

## Files You'll Interact With

| File | Purpose |
|------|---------|
| `app.py` | Main application (updated) |
| `chatbot_data.db` | Messages database (auto-created) |
| `.env` | Configuration (unchanged) |

---

## For Developers

### Key Functions Added:

```python
# Authentication
validate_api_key(api_key)           # Check if key is valid
hash_api_key(api_key)               # Hash for storage

# Database
init_database()                     # Create tables
save_message(session_id, role, content)    # Store message
get_persistent_history(session_id)  # Retrieve messages

# Rate Limiting
check_rate_limit(identifier)        # Check if over limit

# Configuration
RATE_LIMIT_REQUESTS = 100           # Max requests
RATE_LIMIT_WINDOW = 3600            # Per how many seconds
```

### Database Schema:
```sql
-- Messages are stored with timestamps
-- Organized by session_id
-- Accessible via /history endpoint
```

---

## Production Deployment

Before going live, consider:

1. **Change API_KEY_SALT** in `.env`:
   ```
   API_KEY_SALT=your-random-string-here
   ```

2. **Use HTTPS** (add reverse proxy like nginx)

3. **Backup database** regularly

4. **Monitor rate limits** and adjust if needed

5. **Enable logging** for debugging

---

## Support

- **Full docs**: See `FEATURES.md`
- **Implementation details**: See `IMPLEMENTATION.md`
- **Configuration**: See `.env` file
- **Testing**: Run `test_api.ps1`

---

## Questions?

Review `FEATURES.md` for complete API documentation and examples.
