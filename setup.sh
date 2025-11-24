#!/bin/bash
# Setup script for Azure OpenAI Chatbot

set -e  # Exit on error

echo "====== Azure OpenAI Chatbot Setup ======"
echo ""

# Check Python
echo "Checking Python..."
python --version

# Create virtual environment
echo "Creating virtual environment..."
python -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r config/requirements.txt

# Copy example config
if [ ! -f config/.env ]; then
    echo "Copying example configuration..."
    cp config/.env.example config/.env
    echo "⚠️  Please edit config/.env with your credentials"
else
    echo "✓ config/.env already exists"
fi

echo ""
echo "====== Setup Complete ======"
echo ""
echo "Next steps:"
echo "1. Edit config/.env with your Azure OpenAI credentials"
echo "2. Run: python src/app.py"
echo "3. Test with: tests/test_api.ps1 (PowerShell) or curl commands"
echo ""
echo "For more information, see README.md or QUICKSTART.md"
