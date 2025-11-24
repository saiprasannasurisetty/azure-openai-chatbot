# 🚀 Deployment Checklist

Complete guide to deploy your Azure OpenAI Chatbot to production with a public URL.

## Pre-Deployment Setup

- [ ] **Azure Account Created**
  - Sign up at https://azure.microsoft.com/en-us/free/
  - Free trial includes $200 credit

- [ ] **Azure CLI Installed**
  ```bash
  # Windows
  # Download: https://aka.ms/InstallAzureCliWindows
  # Or: choco install azure-cli
  
  # macOS
  brew install azure-cli
  
  # Linux
  curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
  
  # Verify
  az --version
  ```

- [ ] **Docker Installed** (Optional but recommended)
  - https://www.docker.com/products/docker-desktop/
  - For building and testing containers locally

- [ ] **Git Repository Updated**
  - [ ] All code committed and pushed
  - [ ] No uncommitted changes
  - [ ] `.gitignore` configured properly

## Quick Deployment (Choose One)

### Option 1: Automated Script (Recommended) ⭐

**Windows:**
```bash
.\scripts\deploy-azure.bat myResourceGroup chatbot-app eastus
```

**Linux/Mac:**
```bash
bash scripts/deploy-azure.sh myResourceGroup chatbot-app eastus
```

- [ ] Script runs successfully
- [ ] Resource group created
- [ ] Container Registry created
- [ ] Docker image built and pushed
- [ ] App Service created and deployed
- [ ] Public URL displayed

### Option 2: Manual Azure CLI

```bash
# Login
az login

# Create resource group
az group create --name myResourceGroup --location eastus

# Create App Service Plan
az appservice plan create --name chatbot-plan \
  --resource-group myResourceGroup --sku B1 --is-linux

# Create Container Registry
az acr create --resource-group myResourceGroup \
  --name chatbotregistry --sku Basic

# Build and push image
az acr build --registry chatbotregistry \
  --image azure-openai-chatbot:latest .

# Create web app
az webapp create --resource-group myResourceGroup \
  --plan chatbot-plan --name chatbot-app \
  --deployment-container-image-name chatbotregistry.azurecr.io/azure-openai-chatbot:latest
```

- [ ] All commands executed successfully
- [ ] No error messages in output
- [ ] Public URL generated

### Option 3: Docker Compose (Local Testing)

```bash
docker-compose up
```

- [ ] Container starts successfully
- [ ] App responds on http://localhost:8080
- [ ] Health endpoint works

## Post-Deployment Configuration

### Environment Variables

```bash
# Set Azure OpenAI credentials (if using real API)
az webapp config appsettings set \
  --resource-group myResourceGroup \
  --name chatbot-app \
  --settings \
  AZURE_OPENAI_ENDPOINT="https://resource.openai.azure.com/" \
  AZURE_OPENAI_KEY="your-api-key" \
  AZURE_OPENAI_DEPLOYMENT="gpt-35-turbo" \
  LOCAL_MODE=false
```

- [ ] Credentials configured (or LOCAL_MODE=true)
- [ ] No errors in configuration

### Verify Deployment

```bash
# Test health endpoint
curl https://chatbot-app.azurewebsites.net/health

# Should return:
# {"status": "ok", "local_mode": false, "azure_configured": true}
```

- [ ] Health endpoint returns 200
- [ ] Status is "ok"
- [ ] Azure configured (if credentials provided)

## Testing Your Deployment

### 1. Generate API Key

```bash
curl -X POST https://chatbot-app.azurewebsites.net/auth/generate-key

# Response:
# {
#   "api_key": "rM5xN_...",
#   "message": "Store this key securely...",
#   "usage": "Authorization: Bearer <api_key>"
# }
```

- [ ] HTTP 201 response
- [ ] API key returned
- [ ] Can copy and store the key

### 2. Send Chat Message

```bash
curl -X POST https://chatbot-app.azurewebsites.net/chat \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "X-Session-ID: test-session-1" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is Azure?"}'

# Response:
# {"from": "local", "session_id": "test-session-1", "response": "..."}
```

- [ ] HTTP 200 response
- [ ] Message response received
- [ ] Session ID in response

### 3. Retrieve History

```bash
curl https://chatbot-app.azurewebsites.net/history \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "X-Session-ID: test-session-1"

# Response:
# {
#   "session_id": "test-session-1",
#   "history": [...],
#   "total_messages": 2
# }
```

- [ ] HTTP 200 response
- [ ] History contains previous messages
- [ ] Message count is correct

## Optional: GitHub Actions CI/CD

For automatic deployment on every GitHub push:

### 1. Create Service Principal

```bash
az ad sp create-for-rbac --name github-actions \
  --role contributor \
  --scopes /subscriptions/{subscription-id}

# Copy entire output
```

- [ ] Command executed
- [ ] JSON output visible
- [ ] Credentials noted

### 2. Add GitHub Secrets

1. Go to GitHub repository → Settings → Secrets
2. Add secrets:
   - `AZURE_CREDENTIALS` - Full JSON output from above
   - `AZURE_APP_NAME` - Your app name (chatbot-app)
   - `AZURE_RESOURCE_GROUP` - Your resource group name

- [ ] AZURE_CREDENTIALS added
- [ ] AZURE_APP_NAME added
- [ ] AZURE_RESOURCE_GROUP added

### 3. Test CI/CD

```bash
# Make a change and push
git add .
git commit -m "test: trigger CI/CD"
git push

# Check GitHub Actions
# Go to Actions tab and verify deployment workflow runs
```

- [ ] GitHub Actions workflow triggered
- [ ] Tests passed
- [ ] Deployment succeeded
- [ ] New version live in minutes

## Monitoring & Maintenance

### View Logs

```bash
# Real-time logs
az webapp log tail --resource-group myResourceGroup --name chatbot-app

# Stop with Ctrl+C
```

- [ ] Can see application logs
- [ ] No error messages (if everything working)

### Check Metrics

```bash
az webapp metrics list --resource-group myResourceGroup --name chatbot-app
```

- [ ] App is running
- [ ] Request count visible
- [ ] Response times reasonable

### Set Up Alerts (Optional)

```bash
# Email alerts on errors
az monitor metrics alert create \
  --name ChatbotErrors \
  --resource-group myResourceGroup \
  --scopes /subscriptions/.../chatbot-app \
  --criteria "avg http_error_500 > 0"
```

- [ ] Alert configuration created (optional)

## Sharing Your Deployment

### Public URL

Your app is now publicly accessible at:

```
https://chatbot-app.azurewebsites.net
```

**Share these endpoints:**

| Endpoint | Purpose | Authentication |
|----------|---------|-----------------|
| `/health` | Health check | None |
| `/auth/generate-key` | Create API key | None |
| `/chat` | Send message | API Key required |
| `/history` | Get conversation | API Key required |

- [ ] URL works in browser
- [ ] Health endpoint accessible
- [ ] Can share URL with others

### Documentation to Share

1. **For Developers**: Link to [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
2. **For Users**: Link to [docs/QUICKSTART.md](docs/QUICKSTART.md)
3. **For API Integration**: Link to [docs/FEATURES.md](docs/FEATURES.md)

- [ ] Documentation links prepared
- [ ] Examples tested
- [ ] Ready to share

## Cost Management

### Monitor Spending

```bash
# Check current usage
az billing usage list --resource-group myResourceGroup

# Set spending limit
az account update --set subscriptionPolicies.spendingLimit=100
```

- [ ] Aware of monthly costs (~$17/month for B1 plan)
- [ ] Spending alerts configured

### Cost Optimization Tips

- [ ] Using B1 plan (good for dev/test)
- [ ] Consider P1V2 for production ($73/month)
- [ ] Enable auto-shutdown during off-hours (if dev)
- [ ] Use Azure DevOps for long-term cost tracking

## Troubleshooting

### App Won't Start

```bash
# Check logs
az webapp log tail --resource-group myResourceGroup --name chatbot-app

# Restart
az webapp restart --resource-group myResourceGroup --name chatbot-app

# Check health
curl https://chatbot-app.azurewebsites.net/health
```

- [ ] Identified and resolved issue
- [ ] App responding to requests

### 503 Service Unavailable

- [ ] Wait 2-3 minutes (cold start after deployment)
- [ ] Container may still be starting
- [ ] Check logs with `az webapp log tail`

### High Latency

- [ ] First request after deployment is slow (cold start)
- [ ] Consider upgrading plan if persistent
- [ ] Check Application Insights for profiling

- [ ] Issue identified and resolved

## Final Checklist

- [ ] Azure deployment complete
- [ ] Public URL accessible
- [ ] API endpoints responding
- [ ] Authentication working
- [ ] Messages persisting in database
- [ ] Monitoring configured (optional)
- [ ] Documentation ready to share
- [ ] Team informed of public URL

## Success! 🎉

Your Azure OpenAI Chatbot is now live on the internet!

**Next Steps:**
1. Share the public URL: `https://chatbot-app.azurewebsites.net`
2. Share API documentation: `docs/FEATURES.md`
3. Monitor usage and costs
4. Update as needed with new features

**For Production:**
- [ ] Set up SSL/TLS certificate (auto with .azurewebsites.net)
- [ ] Configure custom domain (optional)
- [ ] Set up continuous backup
- [ ] Enable Azure Advisor recommendations
- [ ] Configure Azure Security Center

---

**Questions?** See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed troubleshooting.

**Ready to scale?** See scaling guide in [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md#scaling).
