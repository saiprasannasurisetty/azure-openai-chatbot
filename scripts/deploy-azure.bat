@echo off
REM Deploy to Azure App Service (Windows batch version)
REM Usage: deploy-azure.bat <resource-group> <app-name> [location]

setlocal enabledelayedexpansion

if "%~2"=="" (
    echo Usage: %0 ^<resource-group^> ^<app-name^> [location]
    echo Example: %0 myResourceGroup chatbot-app eastus
    exit /b 1
)

set RESOURCE_GROUP=%~1
set APP_NAME=%~2
set LOCATION=%~3
if "!LOCATION!"=="" set LOCATION=eastus

echo.
echo Deploying Azure OpenAI Chatbot to Azure App Service
echo Resource Group: !RESOURCE_GROUP!
echo App Name: !APP_NAME!
echo Location: !LOCATION!
echo.

REM Check if Azure CLI is installed
where az >nul 2>nul
if errorlevel 1 (
    echo Error: Azure CLI is not installed. Please install it first.
    echo Visit: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli
    exit /b 1
)

REM Login to Azure
echo Logging in to Azure...
call az login
if errorlevel 1 goto error

REM Create resource group
echo Creating resource group: !RESOURCE_GROUP!
call az group create --name "!RESOURCE_GROUP!" --location "!LOCATION!"
if errorlevel 1 goto error

REM Create App Service plan
echo Creating App Service plan...
set PLAN_NAME=!APP_NAME!-plan
call az appservice plan create --name "!PLAN_NAME!" --resource-group "!RESOURCE_GROUP!" --sku B1 --is-linux
if errorlevel 1 goto error

REM Create Container Registry
echo Creating Container Registry...
for /f %%i in ('echo !APP_NAME!-registry ^| findstr /v "-"') do set REGISTRY_NAME=%%i
call az acr create --resource-group "!RESOURCE_GROUP!" --name "!REGISTRY_NAME!" --sku Basic
if errorlevel 1 goto error

REM Get registry URL
for /f %%i in ('az acr show --name "!REGISTRY_NAME!" --query loginServer -o tsv') do set REGISTRY_URL=%%i

REM Build and push Docker image
echo Building Docker image...
call az acr build --registry "!REGISTRY_NAME!" --image "azure-openai-chatbot:latest" .
if errorlevel 1 goto error

set IMAGE_NAME=!REGISTRY_URL!/azure-openai-chatbot:latest

REM Create web app
echo Creating web app: !APP_NAME!
call az webapp create --resource-group "!RESOURCE_GROUP!" --plan "!PLAN_NAME!" --name "!APP_NAME!" --deployment-container-image-name "!IMAGE_NAME!"
if errorlevel 1 goto error

REM Get registry credentials
for /f %%i in ('az acr credential show --name "!REGISTRY_NAME!" --query username -o tsv') do set REGISTRY_USERNAME=%%i
for /f %%i in ('az acr credential show --name "!REGISTRY_NAME!" --query "passwords[0].value" -o tsv') do set REGISTRY_PASSWORD=%%i

REM Configure container registry
echo Configuring container registry credentials...
call az webapp config container set --name "!APP_NAME!" --resource-group "!RESOURCE_GROUP!" --docker-custom-image-name "!IMAGE_NAME!" --docker-registry-server-url "https://!REGISTRY_URL!" --docker-registry-server-user "!REGISTRY_USERNAME!" --docker-registry-server-password "!REGISTRY_PASSWORD!"
if errorlevel 1 goto error

REM Configure environment variables
echo Configuring environment variables...
call az webapp config appsettings set --resource-group "!RESOURCE_GROUP!" --name "!APP_NAME!" --settings WEBSITES_ENABLE_APP_SERVICE_STORAGE=false WEBSITES_PORT=8080 LOCAL_MODE=true
if errorlevel 1 goto error

REM Get app URL
for /f %%i in ('az webapp show --resource-group "!RESOURCE_GROUP!" --name "!APP_NAME!" --query defaultHostName -o tsv') do set APP_URL=%%i

echo.
echo Deployment completed successfully!
echo.
echo Public URL: https://!APP_URL!
echo.
echo Next steps:
echo 1. Test health endpoint: curl https://!APP_URL!/health
echo 2. Generate API key: curl -X POST https://!APP_URL!/auth/generate-key
echo 3. Check logs: az webapp log tail --resource-group !RESOURCE_GROUP! --name !APP_NAME!
echo.
goto end

:error
echo Error occurred during deployment!
exit /b 1

:end
endlocal
