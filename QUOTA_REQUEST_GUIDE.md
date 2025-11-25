# 🎯 Azure Quota Increase Request Guide

## Quick Summary
Your subscription needs **1 Basic VM quota** in **eastus** region to deploy the chatbot to Azure App Service.

---

## 📋 Step-by-Step Instructions

### Step 1: Go to Azure Portal
1. Open: https://portal.azure.com
2. Sign in with: `saiprasannasurisetty@gmail.com`
3. Search for: **"Quotas"** (top search bar)

### Step 2: Navigate to Compute Quotas
1. Click on **"Quotas"** service
2. In the left sidebar, select **"Compute"**
3. Look for **"App Service"** in the provider list
4. Click on **"App Service"**

### Step 3: Request Increase
1. Filter by **Location**: `East US (eastus)`
2. Find the row: **"Cores - Basic instances"**
3. Current Limit: 0
4. Required for deployment: **1**
5. Click the **checkmark** to select it
6. Click **"Request quota increase"** button at top

### Step 4: Fill Request Form
1. **New limit**: Enter `1`
2. **Description**: "Need 1 Basic VM for Azure OpenAI Chatbot deployment"
3. Click **"Request"**
4. Azure sends confirmation email

### Step 5: Wait for Approval
- Approval usually takes: **2-24 hours**
- You'll receive email confirmation when approved
- Quota becomes available immediately after approval

---

## ✅ After Approval

Once approved, run this command to complete deployment:

```powershell
# Set Azure path
$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User")

# Go to project folder
cd "C:\Users\saipr\Documents\GitHub\azure-openai-chatbot"

# Deploy to Azure
.\scripts\deploy-azure.bat myResourceGroup chatbot-app eastus
```

This will:
- Create App Service Plan (B1 - $12/month)
- Deploy your chatbot
- Return public URL: `https://chatbot-app.azurewebsites.net`

---

## 💡 Alternative: Try Different Region

If you want to deploy **now** without waiting:

```powershell
$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User")

# Try West US 2 instead of East US
az appservice plan create --name chatbot-plan --resource-group myResourceGroup --sku B1 --is-linux --location westus2
```

Regions to try:
- `westus2` - West US 2
- `northcentralus` - North Central US
- `southcentralus` - South Central US

---

## 📞 Need Help?

If request is denied or takes too long:
1. Contact Azure Support: https://portal.azure.com/support/create
2. Create case with: "Need VM quota for App Service deployment"
3. Include subscription ID: `f6800f09-c6eb-4453-a3d6-38b38e853aa3`

---

## 🔄 Automatic Deployment When Approved

Once quota is approved, you can use GitHub Actions for automatic deployment:
- See `GITHUB_ACTIONS_SETUP.md` for automation setup
- Your code will deploy automatically to Azure on every `git push`

