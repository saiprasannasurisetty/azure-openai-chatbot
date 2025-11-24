# 🚀 Deploy Now - Quick Start Guide

Your Azure OpenAI Chatbot is ready to deploy! Follow these 5 steps to get your public URL.

## Step 1: Install Azure CLI (5 minutes)

### Windows
**Option A: Direct Download (Easiest)**
```
https://aka.ms/InstallAzureCliWindows
```
1. Click link above
2. Download installer
3. Run it and follow prompts
4. Restart your terminal

**Option B: Via Package Manager**
```bash
# If you have Chocolatey:
choco install azure-cli

# If you have Windows 11 Package Manager:
winget install Microsoft.AzureCLI
```

**Option C: Automatic (Run this script)**
```bash
.\scripts\install-azure-cli.bat
```

### macOS
```bash
brew install azure-cli
```

### Linux
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

## Step 2: Verify Installation

```bash
az --version
```

You should see version information. If not, restart your terminal.

## Step 3: Login to Azure

```bash
az login
```

This will open your browser to login to Azure. If you don't have an account, create a free one:
https://azure.microsoft.com/en-us/free/

## Step 4: Deploy to Azure

### Quick Deploy (Windows)
```bash
.\scripts\deploy-azure.bat myResourceGroup chatbot-app eastus
```

### Quick Deploy (macOS/Linux)
```bash
bash scripts/deploy-azure.sh myResourceGroup chatbot-app eastus
```

**What happens:**
- ✅ Creates Azure Resource Group
- ✅ Creates Container Registry
- ✅ Builds Docker image
- ✅ Pushes to registry
- ✅ Creates App Service
- ✅ Deploys your app
- ✅ Returns public URL

**Time**: ~5-10 minutes

## Step 5: Access Your Public URL

The script will display your public URL:

```
https://chatbot-app.azurewebsites.net
```

### Test It Immediately

```bash
# 1. Health check
curl https://chatbot-app.azurewebsites.net/health

# 2. Generate API key
curl -X POST https://chatbot-app.azurewebsites.net/auth/generate-key

# 3. Save the API key and chat!
curl -X POST https://chatbot-app.azurewebsites.net/chat \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "X-Session-ID: session-1" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello! What can you do?"}'
```

## 💰 Cost

- **Monthly**: ~$17/month (App Service $12 + Registry $5)
- **First month**: Often free or heavily discounted
- **Free trial**: $200 credit included

## 🎯 After Deployment

### Share Your URL
```
https://chatbot-app.azurewebsites.net
```

### Monitor Logs
```bash
az webapp log tail --resource-group myResourceGroup --name chatbot-app
```

### Update Settings
```bash
az webapp config appsettings set \
  --resource-group myResourceGroup \
  --name chatbot-app \
  --settings AZURE_OPENAI_ENDPOINT=https://... \
  AZURE_OPENAI_KEY=your-key \
  AZURE_OPENAI_DEPLOYMENT=gpt-35-turbo
```

### Check Deployment Status
```bash
az webapp show --resource-group myResourceGroup --name chatbot-app
```

## ❓ Troubleshooting

### "az: command not found"
- Azure CLI not installed or not in PATH
- Restart terminal after installation
- Run: `.\scripts\install-azure-cli.bat`

### "Must authenticate first"
- Run: `az login`
- Complete browser authentication

### Deployment hangs
- Wait 3-5 minutes (first deployment is slow)
- Check logs: `az webapp log tail ...`

### Container won't start
- Check logs for errors
- Verify environment variables are set
- Restart: `az webapp restart ...`

## 📚 More Information

- **Full Guide**: `docs/DEPLOYMENT.md`
- **Checklist**: `DEPLOYMENT_CHECKLIST.md`
- **Configuration**: `docs/AZURE_SETUP.md`

## 🔄 Continuous Deployment (Optional)

For automatic deployment on every GitHub push:

1. Create service principal:
```bash
az ad sp create-for-rbac --name github-actions --role contributor
```

2. Add GitHub Secrets (copy output above):
   - `AZURE_CREDENTIALS` (entire JSON)
   - `AZURE_APP_NAME` (chatbot-app)
   - `AZURE_RESOURCE_GROUP` (myResourceGroup)

3. Push code and it deploys automatically! ✨

## 🎉 You're Ready!

Your chatbot will be live on the internet with a public HTTPS URL in minutes.

**Ready? Start with Step 1 above!** 🚀
