#!/bin/bash
# Deploy to Azure App Service
# Usage: ./scripts/deploy-azure.sh <resource-group> <app-name>

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check arguments
if [ $# -lt 2 ]; then
    echo -e "${RED}Usage: $0 <resource-group> <app-name>${NC}"
    echo "Example: $0 myResourceGroup chatbot-app"
    exit 1
fi

RESOURCE_GROUP=$1
APP_NAME=$2
LOCATION=${3:-"eastus"}

echo -e "${YELLOW}Deploying Azure OpenAI Chatbot to Azure App Service${NC}"
echo "Resource Group: $RESOURCE_GROUP"
echo "App Name: $APP_NAME"
echo "Location: $LOCATION"
echo ""

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo -e "${RED}Error: Azure CLI is not installed. Please install it first.${NC}"
    echo "Visit: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Login to Azure
echo -e "${YELLOW}Logging in to Azure...${NC}"
az login

# Create resource group
echo -e "${YELLOW}Creating resource group: $RESOURCE_GROUP${NC}"
az group create \
    --name "$RESOURCE_GROUP" \
    --location "$LOCATION"

# Create App Service plan
echo -e "${YELLOW}Creating App Service plan...${NC}"
PLAN_NAME="${APP_NAME}-plan"
az appservice plan create \
    --name "$PLAN_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --sku B1 \
    --is-linux

# Create Azure Container Registry (optional, for image storage)
echo -e "${YELLOW}Creating Container Registry...${NC}"
REGISTRY_NAME=$(echo "${APP_NAME}registry" | tr '-' '')
az acr create \
    --resource-group "$RESOURCE_GROUP" \
    --name "$REGISTRY_NAME" \
    --sku Basic

# Get registry credentials
echo -e "${YELLOW}Getting registry credentials...${NC}"
REGISTRY_URL=$(az acr show \
    --name "$REGISTRY_NAME" \
    --query loginServer \
    --output tsv)

# Build and push Docker image
echo -e "${YELLOW}Building Docker image...${NC}"
IMAGE_NAME="${REGISTRY_URL}/azure-openai-chatbot:latest"
az acr build \
    --registry "$REGISTRY_NAME" \
    --image "azure-openai-chatbot:latest" \
    .

# Create web app
echo -e "${YELLOW}Creating web app: $APP_NAME${NC}"
az webapp create \
    --resource-group "$RESOURCE_GROUP" \
    --plan "$PLAN_NAME" \
    --name "$APP_NAME" \
    --deployment-container-image-name "$IMAGE_NAME"

# Configure container registry
echo -e "${YELLOW}Configuring container registry credentials...${NC}"
REGISTRY_USERNAME=$(az acr credential show \
    --name "$REGISTRY_NAME" \
    --query "username" \
    --output tsv)
REGISTRY_PASSWORD=$(az acr credential show \
    --name "$REGISTRY_NAME" \
    --query "passwords[0].value" \
    --output tsv)

az webapp config container set \
    --name "$APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --docker-custom-image-name "$IMAGE_NAME" \
    --docker-registry-server-url "https://${REGISTRY_URL}" \
    --docker-registry-server-user "$REGISTRY_USERNAME" \
    --docker-registry-server-password "$REGISTRY_PASSWORD"

# Configure environment variables
echo -e "${YELLOW}Configuring environment variables...${NC}"
az webapp config appsettings set \
    --resource-group "$RESOURCE_GROUP" \
    --name "$APP_NAME" \
    --settings \
    WEBSITES_ENABLE_APP_SERVICE_STORAGE=false \
    WEBSITES_PORT=8080 \
    LOCAL_MODE=true

# Optional: Configure Azure OpenAI credentials
echo -e "${YELLOW}Configure Azure OpenAI credentials (optional)${NC}"
read -p "Do you want to configure Azure OpenAI? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter AZURE_OPENAI_ENDPOINT: " ENDPOINT
    read -p "Enter AZURE_OPENAI_KEY: " KEY
    read -p "Enter AZURE_OPENAI_DEPLOYMENT: " DEPLOYMENT
    
    az webapp config appsettings set \
        --resource-group "$RESOURCE_GROUP" \
        --name "$APP_NAME" \
        --settings \
        AZURE_OPENAI_ENDPOINT="$ENDPOINT" \
        AZURE_OPENAI_KEY="$KEY" \
        AZURE_OPENAI_DEPLOYMENT="$DEPLOYMENT"
fi

# Get the web app URL
APP_URL=$(az webapp show \
    --resource-group "$RESOURCE_GROUP" \
    --name "$APP_NAME" \
    --query "defaultHostName" \
    --output tsv)

echo -e "${GREEN}Deployment completed successfully!${NC}"
echo ""
echo -e "${GREEN}Public URL: https://${APP_URL}${NC}"
echo ""
echo "Next steps:"
echo "1. Test health endpoint: curl https://${APP_URL}/health"
echo "2. Generate API key: curl -X POST https://${APP_URL}/auth/generate-key"
echo "3. Check logs: az webapp log tail --resource-group $RESOURCE_GROUP --name $APP_NAME"
echo ""
echo "To enable continuous deployment from GitHub:"
echo "  az webapp deployment github-actions add ..."
