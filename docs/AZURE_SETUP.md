# Azure App Service Configuration Template

This file contains example configurations for deploying to Azure App Service.

## app.yml - App Service Configuration

```yaml
apiVersion: 2019-08-01
type: Microsoft.Web/sites
name: chatbot-app
location: eastus

properties:
  serverFarmId: /subscriptions/{id}/resourceGroups/myResourceGroup/providers/Microsoft.Web/serverfarms/chatbot-plan
  
  siteConfig:
    linuxFxVersion: DOCKER|ghcr.io/username/azure-openai-chatbot:latest
    appCommandLine: ""
    
    connectionStrings:
      - name: DATABASE_URL
        connectionString: "postgresql://user:password@host/db"
        type: PostgreSQL
    
    appSettings:
      - name: WEBSITES_ENABLE_APP_SERVICE_STORAGE
        value: "false"
      
      - name: WEBSITES_PORT
        value: "8080"
      
      - name: LOCAL_MODE
        value: "false"
      
      - name: AZURE_OPENAI_ENDPOINT
        value: "https://resource.openai.azure.com/"
      
      - name: AZURE_OPENAI_KEY
        value: "your-api-key"
        slotSetting: false
      
      - name: AZURE_OPENAI_DEPLOYMENT
        value: "gpt-35-turbo"
      
      - name: FLASK_ENV
        value: "production"
      
      - name: PYTHONUNBUFFERED
        value: "1"
    
    numberOfWorkers: 1
    defaultDocuments: []
    netFrameworkVersion: "v4.0"
    requestTracingEnabled: false
    remoteDebuggingEnabled: false
    httpLoggingEnabled: true
    detailedErrorLoggingEnabled: true
    use32BitWorkerProcess: false
    webSocketsEnabled: false
    managedPipelineMode: "Integrated"
    virtualApplications:
      - virtualPath: "/"
        physicalPath: "site\\wwwroot"
        preloadEnabled: true

  clientAffinityEnabled: false
  clientCertEnabled: false
  hostNamesDisabled: false
  containerSize: 0
  dailyMemoryTimeQuota: 0
  enabled: true

resources:
  - apiVersion: 2019-08-01
    type: hostBindings
    name: chatbot-app.azurewebsites.net
    properties:
      siteName: chatbot-app
      hostName: chatbot-app.azurewebsites.net
```

## ARM Template (infrastructure-as-code)

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  
  "parameters": {
    "appName": {
      "type": "string",
      "metadata": {"description": "Name of the App Service"}
    },
    "location": {
      "type": "string",
      "defaultValue": "[resourceGroup().location]"
    }
  },
  
  "variables": {
    "appServicePlanName": "[concat(parameters('appName'), '-plan')]",
    "registryName": "[concat(parameters('appName'), 'registry')]"
  },
  
  "resources": [
    {
      "type": "Microsoft.Web/serverfarms",
      "apiVersion": "2021-02-01",
      "name": "[variables('appServicePlanName')]",
      "location": "[parameters('location')]",
      "kind": "linux",
      "sku": {
        "name": "B1",
        "capacity": 1
      },
      "properties": {
        "reserved": true
      }
    },
    
    {
      "type": "Microsoft.Web/sites",
      "apiVersion": "2021-02-01",
      "name": "[parameters('appName')]",
      "location": "[parameters('location')]",
      "dependsOn": [
        "[resourceId('Microsoft.Web/serverfarms', variables('appServicePlanName'))]"
      ],
      "properties": {
        "serverFarmId": "[resourceId('Microsoft.Web/serverfarms', variables('appServicePlanName'))]",
        "siteConfig": {
          "linuxFxVersion": "DOCKER|azure-openai-chatbot:latest",
          "appSettings": [
            {
              "name": "WEBSITES_PORT",
              "value": "8080"
            },
            {
              "name": "LOCAL_MODE",
              "value": "true"
            }
          ]
        }
      }
    }
  ],
  
  "outputs": {
    "appUrl": {
      "type": "string",
      "value": "[concat('https://', parameters('appName'), '.azurewebsites.net')]"
    }
  }
}
```

## GitHub Secrets Required

Add these to GitHub repository settings (Settings → Secrets):

```
AZURE_CREDENTIALS
{
  "clientId": "xxxxxxxx",
  "clientSecret": "xxxxxxxx",
  "subscriptionId": "xxxxxxxx",
  "tenantId": "xxxxxxxx",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.microsoft.com/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}

AZURE_APP_NAME=chatbot-app
AZURE_RESOURCE_GROUP=myResourceGroup
```

## Environment-Specific Configurations

### Development
```
LOCAL_MODE=true
FLASK_ENV=development
DEBUG=true
```

### Staging
```
LOCAL_MODE=false
FLASK_ENV=staging
DEBUG=false
DATABASE_URL=postgresql://...
```

### Production
```
LOCAL_MODE=false
FLASK_ENV=production
DEBUG=false
DATABASE_URL=postgresql://...
AZURE_OPENAI_ENDPOINT=https://resource.openai.azure.com/
AZURE_OPENAI_KEY=<key>
AZURE_OPENAI_DEPLOYMENT=gpt-35-turbo
```

## Health Check Configuration

App Service health check (improves reliability):

```bash
az webapp config set --resource-group myResourceGroup \
  --name chatbot-app \
  --generic-configurations '{"healthCheckPath":"/health"}'
```

## Deployment Slots

For zero-downtime deployments:

```bash
# Create slot
az webapp deployment slot create --name chatbot-app \
  --resource-group myResourceGroup \
  --slot staging

# Deploy to staging
# ... (deploy container to staging)

# Swap slots
az webapp deployment slot swap --name chatbot-app \
  --resource-group myResourceGroup \
  --slot staging
```

## Monitoring Setup

```bash
# Create Application Insights
az monitor app-insights component create \
  --app chatbot-insights \
  --location eastus \
  --resource-group myResourceGroup \
  --application-type web

# Get instrumentation key
IKEY=$(az monitor app-insights component show \
  --app chatbot-insights \
  --resource-group myResourceGroup \
  --query instrumentationKey -o tsv)

# Link to App Service
az webapp config appsettings set \
  --name chatbot-app \
  --resource-group myResourceGroup \
  --settings APPINSIGHTS_INSTRUMENTATIONKEY=$IKEY
```
