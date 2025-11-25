# 🚀 GitHub Actions Automation Setup

This guide walks you through setting up **automatic deployment** to Azure. Every time you push code to `main` branch, your app automatically deploys!

---

## 📋 Prerequisites

✅ Azure subscription (free tier works)
✅ Azure CLI installed (we already did this)
✅ GitHub repository (already have: `saiprasannasurisetty/azure-openai-chatbot`)
✅ **VM Quota approved** (for B1 plan) - See `QUOTA_REQUEST_GUIDE.md`

---

## ⚙️ Setup Steps

### Step 1: Create Azure Service Principal

This lets GitHub authenticate with Azure.

```powershell
# Set Azure path
$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User")

# Create service principal
az ad sp create-for-rbac --name github-actions --role contributor

# Copy the entire output (you'll need it in Step 2)
```

**Output will look like:**
```json
{
  "clientId": "00000000-0000-0000-0000-000000000000",
  "clientSecret": "xxxx-xxxx-xxxx-xxxx",
  "subscriptionId": "f6800f09-c6eb-4453-a3d6-38b38e853aa3",
  "tenantId": "00000000-0000-0000-0000-000000000000",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}
```

**⚠️ IMPORTANT: Save this output! You'll need it next.**

---

### Step 2: Add GitHub Secrets

GitHub Secrets are encrypted environment variables only GitHub Actions can access.

#### Steps:
1. Go to your GitHub repo: https://github.com/saiprasannasurisetty/azure-openai-chatbot
2. Click **Settings** (top menu)
3. Left sidebar → Click **"Secrets and variables"** → **"Actions"**
4. Click **"New repository secret"** button

#### Add 4 Secrets:

**Secret 1: AZURE_CREDENTIALS**
- Name: `AZURE_CREDENTIALS`
- Value: Paste the **entire JSON** from Step 1
- Click **"Add secret"**

**Secret 2: AZURE_RESOURCE_GROUP**
- Name: `AZURE_RESOURCE_GROUP`
- Value: `myResourceGroup`
- Click **"Add secret"**

**Secret 3: AZURE_APP_NAME**
- Name: `AZURE_APP_NAME`
- Value: `chatbot-app`
- Click **"Add secret"**

**Secret 4: AZURE_OPENAI_* (Optional - only if using real Azure OpenAI)**
- Name: `AZURE_OPENAI_ENDPOINT`
- Value: `https://your-resource.openai.azure.com/`
- Name: `AZURE_OPENAI_KEY`
- Value: `your-api-key`
- Name: `AZURE_OPENAI_DEPLOYMENT`
- Value: `gpt-35-turbo`

**Or set LOCAL_MODE:**
```yaml
# In workflow file, change line to:
LOCAL_MODE=true
```

---

### Step 3: Verify Workflow File Exists

The workflow file should be at: `.github/workflows/deploy-to-azure.yml`

✅ Already created for you! It's in the repo.

---

## 🎯 How It Works

### 1. You Push Code
```powershell
cd "C:\Users\saipr\Documents\GitHub\azure-openai-chatbot"
git add .
git commit -m "Update chatbot feature"
git push origin main
```

### 2. GitHub Actions Triggers
Automatically runs the workflow defined in `.github/workflows/deploy-to-azure.yml`

### 3. Automatic Deployment
- ✅ Creates Azure resources (if needed)
- ✅ Builds and deploys your app
- ✅ Returns public URL
- ✅ Runs health tests

### 4. App is Live
Your app is now running at: `https://chatbot-app.azurewebsites.net`

---

## 📊 Monitor Deployments

### View Workflow Runs
1. Go to your GitHub repo
2. Click **"Actions"** tab
3. See all deployment runs with status (✅ or ❌)
4. Click any run to see detailed logs

### Check Logs
- View step-by-step execution
- Debug failures
- See deployment URL at the end

---

## 🔄 Trigger Manual Deployment

Even without pushing code, you can manually trigger deployment:

1. Go to **Actions** tab
2. Select **"Deploy to Azure"** workflow
3. Click **"Run workflow"** button
4. Choose branch: `main`
5. Click **"Run workflow"**

---

## ✨ First Deployment - Quick Start

```powershell
# 1. Verify all files exist
ls .github/workflows/deploy-to-azure.yml

# 2. Make a small change
# Edit any file, e.g., README.md

# 3. Commit and push
git add .
git commit -m "Trigger first deployment"
git push origin main

# 4. Watch it deploy
# Go to: https://github.com/saiprasannasurisetty/azure-openai-chatbot/actions
# Click the latest run to see live logs
```

---

## 🧪 Test Your Deployment

Once workflow completes, test your app:

```powershell
# 1. Health check
curl https://chatbot-app.azurewebsites.net/health

# 2. Generate API key
$response = Invoke-WebRequest -Uri "https://chatbot-app.azurewebsites.net/auth/generate-key" -Method POST
$response.Content | ConvertFrom-Json

# 3. Send test message
$apiKey = "YOUR_KEY_FROM_STEP_2"
Invoke-WebRequest -Uri "https://chatbot-app.azurewebsites.net/chat" -Method POST `
  -Headers @{
    "Authorization" = "Bearer $apiKey"
    "X-Session-ID" = "test-1"
    "Content-Type" = "application/json"
  } -Body '{"prompt": "Hello"}'
```

---

## 🛑 Disable Workflow (Temporarily)

If you need to stop auto-deployment:

1. Go to **Actions** tab
2. Click **"Deploy to Azure"** workflow
3. Click **"..."** menu
4. Click **"Disable workflow"**

To re-enable:
1. Click **"Enable workflow"** button

---

## 🐛 Troubleshooting

### Workflow Fails with "Quota Exceeded"
- **Problem**: VM quota not approved yet
- **Solution**: Wait for quota approval (24 hours), then re-run
- **Rerun**: Go to Actions → Latest run → Click "Re-run all jobs"

### "Invalid credentials"
- **Problem**: AZURE_CREDENTIALS secret is wrong
- **Solution**: 
  1. Recreate service principal: `az ad sp create-for-rbac --name github-actions --role contributor`
  2. Update AZURE_CREDENTIALS secret with new JSON
  3. Re-run workflow

### "Resource group already exists"
- **Problem**: Not actually an error, workflow continues
- **Solution**: None needed, workflow handles this gracefully

### Deployment takes too long (> 10 min)
- **Problem**: Normal for first deployment (cold start)
- **Solution**: Subsequent deployments are faster (~3-5 min)

---

## 📱 Share Your Live App

Once deployed, share this URL with others:

```
https://chatbot-app.azurewebsites.net
```

**For API access, they need:**
1. Generate API key: `https://chatbot-app.azurewebsites.net/auth/generate-key`
2. Use in requests: `Authorization: Bearer <key>`

---

## 🔄 Workflow File Details

The workflow does:

| Step | Action |
|------|--------|
| **Checkout** | Clone your code |
| **Azure Login** | Authenticate with service principal |
| **Create Resource Group** | Create `myResourceGroup` (if needed) |
| **Create App Service Plan** | Create `chatbot-plan` (B1 Linux) |
| **Create Web App** | Create `chatbot-app` |
| **Configure Settings** | Set environment variables |
| **Deploy Code** | Upload your code to Azure |
| **Test** | Verify app is responding |
| **Summary** | Show deployment URL |

---

## 💡 Advanced: Customize Deployment

### Change App Name
Edit `.github/workflows/deploy-to-azure.yml`:
```yaml
# Change line:
--name my-custom-app-name
```

### Change Resource Group
Edit GitHub secret `AZURE_RESOURCE_GROUP`:
- Go to Secrets
- Change value to new name
- Next deployment uses new group

### Add Custom Configuration
In workflow file, add to "Configure App Settings" step:
```yaml
MY_CUSTOM_VAR=my_value
```

---

## 🎉 Next Steps

1. **Now**: Ensure quota is approved (or request if not)
2. **Push code**: Any change to `main` triggers deployment
3. **Monitor**: Check Actions tab for deployment status
4. **Test**: Use public URL to test your app
5. **Share**: Send URL to others to use your chatbot

---

## ✅ Checklist

- [ ] Service principal created (Step 1)
- [ ] AZURE_CREDENTIALS secret added
- [ ] AZURE_RESOURCE_GROUP secret added
- [ ] AZURE_APP_NAME secret added
- [ ] Workflow file exists at `.github/workflows/deploy-to-azure.yml`
- [ ] VM quota requested (if needed)
- [ ] Ready to push code and trigger deployment

**All done? Push your code and watch it deploy automatically!** 🚀

