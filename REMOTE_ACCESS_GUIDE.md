# 🌐 Remote Access Setup - Access Your Local App Anywhere

Your chatbot is currently running locally on your machine. You can access it from anywhere using these methods:

---

## Method 1: Ngrok (Easiest - Instant Public URL) ⭐

### What is Ngrok?
Ngrok creates a public HTTPS URL that tunnels to your local machine. Perfect for quick demos.

### Step 1: Download Ngrok
1. Visit: https://ngrok.com/download
2. Download for Windows
3. Extract to a folder (e.g., `C:\ngrok`)

### Step 2: Start Your App (if not running)
```powershell
cd "C:\Users\saipr\Documents\GitHub\azure-openai-chatbot"
.venv\Scripts\Activate.ps1
$env:LOCAL_MODE="true"
python src/app.py
```

App runs on: `http://127.0.0.1:8080`

### Step 3: Create Ngrok Tunnel
```powershell
# Open new PowerShell terminal
cd C:\ngrok
.\ngrok http 8080
```

You'll see:
```
Forwarding:  https://abc123-def456.ngrok.io -> http://localhost:8080
```

**Your public URL is:** `https://abc123-def456.ngrok.io`

### Step 4: Test from Anywhere
```bash
# Test health check
curl https://abc123-def456.ngrok.io/health

# Generate API key
curl -X POST https://abc123-def456.ngrok.io/auth/generate-key

# Send message
curl -X POST https://abc123-def456.ngrok.io/chat \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "X-Session-ID: test" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello!"}'
```

### ⚠️ Important Notes
- URL changes every time ngrok restarts
- Free tier has rate limits
- Perfect for demos and testing
- Keep terminal open while in use

---

## Method 2: Cloudflare Tunnel (Free & Persistent) ✅

### What is Cloudflare Tunnel?
Provides persistent URL + no port forwarding needed. Better than ngrok for long-term use.

### Step 1: Install Cloudflare Tunnel
```powershell
# Download from: https://github.com/cloudflare/cloudflared/releases
# Download: cloudflared-windows-amd64.exe

# Move to system path or navigate to it
cd "C:\Users\saipr\Downloads" # or wherever downloaded
.\cloudflared-windows-amd64.exe tunnel --url http://localhost:8080
```

### Step 2: Get Your URL
Output will show:
```
INF Tunnel credentials have been saved in C:\Users\saipr\.cloudflared
INF Attempting to connect to the Cloudflare edge with your delegation token...
INF |  Your quick Tunnel has been created! Visit it at (it will begin routing your requests):
INF |  https://your-unique-url.trycloudflare.com
```

**Your public URL:** `https://your-unique-url.trycloudflare.com`

### Step 3: Keep Running
Keep terminal open. This URL persists and works as long as cloudflared is running.

---

## Method 3: Windows Remote Desktop + Port Forwarding

### Step 1: Enable Remote Desktop
```powershell
# Run as Administrator
Enable-NetFirewallRule -DisplayGroup "Remote Desktop"
```

### Step 2: Find Your IP
```powershell
ipconfig
# Look for: IPv4 Address (e.g., 192.168.1.100)
```

### Step 3: Access from Another Machine
- Use RDP client to connect: `192.168.1.100:3389`
- Then access app on that machine: `http://localhost:8080`

---

## Method 4: Port Forwarding on Router (Permanent)

### For Permanent Public Access
1. Log into your router (usually 192.168.1.1)
2. Find "Port Forwarding" settings
3. Forward external port 8080 → local machine:8080
4. Get your public IP: https://whatismyipaddress.com
5. Access from anywhere: `http://YOUR_PUBLIC_IP:8080`

⚠️ **Security Warning**: This exposes your local machine. Better to wait for Azure deployment.

---

## Method 5: Tailscale VPN (Secure Private Network)

### Step 1: Download Tailscale
Visit: https://tailscale.com/download

### Step 2: Install & Login
```powershell
# Install and run Tailscale
# Your machine joins secure VPN
```

### Step 3: Access from Other Tailscale Devices
Your Tailscale IP: (shown in Tailscale app)
```
Access: http://YOUR_TAILSCALE_IP:8080
```

All traffic encrypted through Tailscale servers. Most secure option.

---

## 🎯 Quick Comparison

| Method | Cost | Setup Time | Persistent URL | Security | Best For |
|--------|------|-----------|-----------------|----------|----------|
| Ngrok | Free | 5 min | ❌ No | 🟡 Good | Quick demos |
| Cloudflare Tunnel | Free | 5 min | ✅ Yes | ✅ Good | Testing |
| Remote Desktop | Free | 10 min | ❌ No | 🟡 OK | Single device |
| Port Forwarding | Free | 20 min | ✅ Yes | 🔴 Risky | Permanent (not recommended) |
| Tailscale | Free | 10 min | ✅ Yes | ✅ Best | Secure access |

---

## 📱 Share Your Public URL

Once you have a URL, you can share it:

```
# Public URL
https://abc123.ngrok.io

# Usage:
1. Get API key:
   https://abc123.ngrok.io/auth/generate-key

2. Send message:
   curl -X POST https://abc123.ngrok.io/chat \
     -H "Authorization: Bearer YOUR_KEY" \
     -H "X-Session-ID: session-1" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Hello!"}'
```

---

## 🔄 Keep App Running 24/7

To keep your app running while your computer is asleep:

### Option 1: Keep PC Always On
- Disable sleep: Settings → Power → Never sleep
- Disable screen lock

### Option 2: Run as Windows Service
Use NSSM (Non-Sucking Service Manager):
```powershell
# Download from: https://nssm.cc/download
# Install as service so app restarts automatically
```

### Option 3: Use Task Scheduler
```powershell
# Create scheduled task to restart app daily
New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-Command `"& {
  cd C:\Users\saipr\Documents\GitHub\azure-openai-chatbot
  .venv\Scripts\Activate.ps1
  python src/app.py
}`""
```

---

## ✨ Recommended Workflow

1. **Now (Testing)**: Use Ngrok for quick testing
2. **This Week**: Set up Cloudflare Tunnel for persistent testing
3. **Next Week**: After quota approval, deploy to Azure (permanent)

---

## 📺 Test Your Remote URL

```bash
# 1. Health check
curl https://your-url.com/health

# 2. View Swagger docs (if enabled)
# Visit: https://your-url.com/

# 3. Full test with API key
API_KEY=$(curl -s -X POST https://your-url.com/auth/generate-key | jq -r '.api_key')

curl -X POST https://your-url.com/chat \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Session-ID: remote-test" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What can you do?"}'
```

---

## 🆘 Troubleshooting

### "Connection Refused"
- App not running: Start with `python src/app.py`
- Wrong port: Check app is on 8080

### "Timeout"
- Tunnel service down: Restart ngrok/cloudflared
- Network issue: Check internet connection

### "Invalid API Key"
- Expired key: Generate new one at `/auth/generate-key`
- Wrong format: Use: `Authorization: Bearer <key>`

