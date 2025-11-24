@echo off
REM Azure CLI Installation Helper for Windows
REM Automatically installs Azure CLI if not present

echo.
echo ========================================
echo   Azure CLI Installation Helper
echo ========================================
echo.

REM Check if Azure CLI is already installed
where az >nul 2>nul
if errorlevel 1 (
    echo Azure CLI not found. Installing...
    echo.
    
    REM Check if winget is available (Windows 11+)
    where winget >nul 2>nul
    if errorlevel 0 (
        echo Installing via Windows Package Manager...
        winget install Microsoft.AzureCLI
        if errorlevel 0 (
            echo.
            echo Azure CLI installed successfully!
            goto success
        )
    )
    
    REM Check if Chocolatey is available
    where choco >nul 2>nul
    if errorlevel 0 (
        echo Installing via Chocolatey...
        choco install azure-cli -y
        if errorlevel 0 (
            echo.
            echo Azure CLI installed successfully!
            goto success
        )
    )
    
    REM Manual installation instructions
    echo.
    echo Neither winget nor Chocolatey found.
    echo Please download and install manually:
    echo.
    echo URL: https://aka.ms/InstallAzureCliWindows
    echo.
    echo After installation, restart PowerShell and run:
    echo   az login
    echo   scripts\deploy-azure.bat myResourceGroup chatbot-app eastus
    echo.
    pause
    goto end
) else (
    echo Azure CLI found!
    goto check_version
)

:check_version
az --version >nul 2>nul
if errorlevel 0 (
    echo.
    echo Installed version:
    az --version
    echo.
    goto success
) else (
    goto error
)

:success
echo.
echo Azure CLI is ready!
echo.
echo Next steps:
echo 1. Run: az login
echo 2. Then: .\scripts\deploy-azure.bat myResourceGroup chatbot-app eastus
echo.
pause
goto end

:error
echo.
echo Error checking Azure CLI installation.
echo Please install manually from: https://aka.ms/InstallAzureCliWindows
echo.
pause
goto end

:end
