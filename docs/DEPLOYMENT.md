# Azure Deployment Guide

Deploy your Azure OpenAI Chatbot to Azure App Service with a public URL for production access.

## Table of Contents
- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Deployment Methods](#deployment-methods)
- [Configuration](#configuration)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## Quick Start

### 1-Minute Deployment (Azure CLI)

```bash
# Clone and setup
git clone https://github.com/saiprasannasurisetty/azure-openai-chatbot.git
cd azure-openai-chatbot

# Login to Azure
az login

# Run deployment script (Linux/Mac)
bash scripts/deploy-azure.sh myResourceGroup chatbot-app

# Or on Windows
deploy-azure.bat myResourceGroup chatbot-app
```

Your public URL will be: `https://chatbot-app.azurewebsites.net`

## Prerequisites

### Required
- Azure subscription ([free tier available](https://azure.microsoft.com/en-us/free/))
- Azure CLI installed ([installation guide](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli))
- Docker installed (for building images)
- Git

### Optional
- Azure Storage Account (for persistent data)
- Azure Application Insights (for monitoring)

## Deployment Methods

### Method 1: Automated Deployment (Recommended)

**Easiest option** - Uses provided deployment scripts:

```bash
# Linux/Mac
bash scripts/deploy-azure.sh myResourceGroup chatbot-app eastus

# Windows
deploy-azure.bat myResourceGroup chatbot-app eastus
```

**What it does:**
- Creates resource group and App Service plan
- Builds and pushes Docker image to Azure Container Registry
- Deploys web app with proper configuration
- Sets up environment variables
- Returns public URL

**Resources created:**
- Resource Group
- App Service Plan (B1 - $12/month)
- Container Registry (Basic - $5/month)
- App Service

### Method 2: Manual Deployment (Azure Portal)

1. **Create App Service:**
   ```
   Azure Portal → App Services → Create → Web App
   ```

2. **Configure Container:**
   ```
   Deployment → Deployment Center → Docker Container
   Select: Single Container
   Image source: Docker Hub / Registry
   ```

3. **Set Environment Variables:**
   ```
   Configuration → Application Settings
   - WEBSITES_PORT=8080
   - LOCAL_MODE=true
   - AZURE_OPENAI_ENDPOINT=<your-endpoint>
   - AZURE_OPENAI_KEY=<your-key>
   - AZURE_OPENAI_DEPLOYMENT=<your-deployment>
   ```

4. **Deploy:**
   ```
   Deployment Center → GitHub (select branch)
   ```

### Method 3: Container Registry Deployment

```bash
# Create Container Registry
az acr create --resource-group myResourceGroup \
  --name chatbotregistry --sku Basic

# Build image
az acr build --registry chatbotregistry \
  --image azure-openai-chatbot:latest .

# Create App Service Plan
az appservice plan create --name chatbot-plan \
  --resource-group myResourceGroup \
  --sku B1 --is-linux

# Create Web App
az webapp create --resource-group myResourceGroup \
  --plan chatbot-plan \
  --name chatbot-app \
  --deployment-container-image-name chatbotregistry.azurecr.io/azure-openai-chatbot:latest
```

### Method 4: GitHub Actions (Continuous Deployment)

Automatic deployment on every push to `main` branch:

```yaml
# Automatically triggered by .github/workflows/deploy.yml
# Set secrets in GitHub:
- AZURE_CREDENTIALS (from 'az ad sp create-for-rbac')
- AZURE_APP_NAME (your app service name)
```

**Setup:**
```bash
# Create service principal
az ad sp create-for-rbac --name github-actions \
  --role contributor \
  --scopes /subscriptions/<subscription-id>

# Copy output to GitHub Secrets
```

Then add to GitHub Secrets:
- `AZURE_CREDENTIALS` - Full output from above
- `AZURE_APP_NAME` - Your App Service name

## Configuration

### Environment Variables

Set these in App Service Configuration:

```
AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com/
AZURE_OPENAI_KEY=<your-api-key>
AZURE_OPENAI_DEPLOYMENT=<deployment-name>
LOCAL_MODE=false
PORT=8080
```

### Persistent Storage

**Option 1: Azure Storage (Recommended)**
```bash
# Create storage account
az storage account create --name chatbotstorage \
  --resource-group myResourceGroup --sku Standard_LRS

# Mount in App Service
# Configuration → Path Mappings → Azure Storage Mounts
```

**Option 2: Local App Service Storage**
```bash
az webapp config appsettings set \
  --name chatbot-app \
  --resource-group myResourceGroup \
  --settings WEBSITES_ENABLE_APP_SERVICE_STORAGE=true
```

### Database

For production, migrate from SQLite to PostgreSQL:

```bash
# Create PostgreSQL
az postgres server create \
  --resource-group myResourceGroup \
  --name chatbot-db \
  --admin-user dbadmin

# Update connection string
az webapp config connection-string set \
  --name chatbot-app \
  --resource-group myResourceGroup \
  --connection-string-type PostgreSQL \
  --settings DATABASE_URL=postgres://...
```

## Usage After Deployment

### Health Check
```bash
curl https://chatbot-app.azurewebsites.net/health
# Returns: {"status": "ok"}
```

### Generate API Key
```bash
curl -X POST https://chatbot-app.azurewebsites.net/auth/generate-key
# Returns: {"api_key": "...", "usage": "Authorization: Bearer ..."}
```

### Chat with Chatbot
```bash
curl -X POST https://chatbot-app.azurewebsites.net/chat \
  -H "Authorization: Bearer <api-key>" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is Azure?"}'
```

### Get Chat History
```bash
curl https://chatbot-app.azurewebsites.net/history \
  -H "Authorization: Bearer <api-key>" \
  -H "X-Session-ID: user-session-1"
```

## Monitoring

### View Logs
```bash
# Real-time logs
az webapp log tail --resource-group myResourceGroup \
  --name chatbot-app

# Stream logs
az webapp log streaming start --resource-group myResourceGroup \
  --name chatbot-app
```

### Set Up Application Insights
```bash
# Create insights instance
az monitor app-insights component create \
  --app chatbot-insights \
  --location eastus \
  --resource-group myResourceGroup \
  --application-type web

# Link to App Service
az webapp config set \
  --resource-group myResourceGroup \
  --name chatbot-app \
  --app-insights-key <instrumentation-key>
```

### Metrics
```
Azure Portal → chatbot-app → Metrics
- Request Count
- Response Time
- HTTP Server Errors
- Successful Requests
```

## Cost Optimization

### Pricing Tiers
```
B1 Plan (Recommended for dev/test)
- $12/month
- 1 Core, 1.75 GB RAM
- 240 minutes/day free compute

P1V2 Plan (Production)
- $73/month
- 1 Core, 3.5 GB RAM
- Always on

Free/Shared
- $0/month
- Limited performance
- Shared resources
```

### Cost Reduction Tips
1. Use B1 plan for development ($12/month)
2. Enable auto-scale for traffic spikes
3. Use App Service on Linux (more efficient)
4. Set deployment slots for staging
5. Implement caching with Azure Front Door

```bash
# Scale up if needed
az appservice plan update --name chatbot-plan \
  --resource-group myResourceGroup \
  --sku P1V2
```

## Scaling

### Vertical Scaling (More Power)
```bash
az appservice plan update --name chatbot-plan \
  --resource-group myResourceGroup \
  --sku P1V2
```

### Horizontal Scaling (More Instances)
```bash
az appservice plan update --name chatbot-plan \
  --resource-group myResourceGroup \
  --number-of-workers 3
```

### Auto-Scale Configuration
```bash
az monitor autoscale create \
  --resource-group myResourceGroup \
  --resource chatbot-app \
  --resource-type "Microsoft.Web/sites" \
  --min-count 1 \
  --max-count 5 \
  --target-resource-id /subscriptions/.../chatbot-app
```

## Troubleshooting

### App Won't Start
```bash
# Check logs
az webapp log tail --resource-group myResourceGroup --name chatbot-app

# Restart app
az webapp restart --resource-group myResourceGroup --name chatbot-app

# Check health
curl https://chatbot-app.azurewebsites.net/health
```

### 503 Service Unavailable
- Container may still be starting (wait 2-3 minutes)
- Check logs for errors
- Verify image exists in registry
- Check resource quotas

### 401 Unauthorized
- API key not provided: Add `Authorization: Bearer <key>` header
- Invalid key: Generate new key with `/auth/generate-key`

### High Latency
- Cold start delay (first request after deployment)
- Container warming up (5-10 seconds typical)
- Upgrade App Service plan
- Enable Application Insights to profile

### Database Connection Issues
- Check firewall rules in App Service
- Verify connection string
- Test with `az postgres server firewall-rule create`

## Cleanup

Remove all resources when done:

```bash
# Delete resource group (deletes everything)
az group delete --name myResourceGroup --yes
```

Or individual resources:

```bash
# Delete web app
az webapp delete --name chatbot-app --resource-group myResourceGroup

# Delete App Service plan
az appservice plan delete --name chatbot-plan --resource-group myResourceGroup

# Delete Container Registry
az acr delete --name chatbotregistry --resource-group myResourceGroup
```

## Next Steps

1. ✅ Deploy to Azure App Service
2. 🔒 Set up SSL/TLS certificates (auto-provisioned with .azurewebsites.net)
3. 📊 Configure monitoring and alerts
4. 🔑 Rotate API keys regularly
5. 🚀 Set up continuous deployment
6. 📈 Monitor costs and usage

## Additional Resources

- [Azure App Service Documentation](https://learn.microsoft.com/en-us/azure/app-service/)
- [Docker Container Deployment](https://learn.microsoft.com/en-us/azure/app-service/configure-custom-container)
- [Azure Container Registry](https://learn.microsoft.com/en-us/azure/container-registry/)
- [Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)
