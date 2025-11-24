"""
Azure OpenAI Chatbot – simple Python example

Usage:
  1. Set environment variables:
     - AZURE_OPENAI_ENDPOINT (e.g. https://your-resource-name.openai.azure.com)
     - AZURE_OPENAI_KEY
     - AZURE_DEPLOYMENT_NAME (the deployment or model name configured in Azure OpenAI)

  2. Install dependencies:
     pip install -r requirements.txt

  3. Run:
     python app.py

This script demonstrates a minimal chat loop using the Azure OpenAI REST Chat Completions endpoint.
"""

import os
import requests

ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
API_KEY = os.getenv("AZURE_OPENAI_KEY")
DEPLOYMENT = os.getenv("AZURE_DEPLOYMENT_NAME")  # e.g. "gpt-35-turbo-deployment"

if not ENDPOINT or not API_KEY or not DEPLOYMENT:
    print("ERROR: Please set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, and AZURE_DEPLOYMENT_NAME environment variables.")
    print("See README.md for instructions.")
    exit(1)

API_VERSION = "2023-03-15-preview"  # compatible chat completions API for many Azure deployments
CHAT_URL = f"{ENDPOINT}/openai/deployments/{DEPLOYMENT}/chat/completions?api-version={API_VERSION}"

HEADERS = {
    "api-key": API_KEY,
    "Content-Type": "application/json"
}

def ask_chat(user_input, system_prompt="You are a helpful assistant specializing in Azure + GenAI developer tasks."):
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 500,
        "temperature": 0.2
    }
    resp = requests.post(CHAT_URL, headers=HEADERS, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    # Azure returns choices -> each has message with role/content
    return data["choices"][0]["message"]["content"]

def main():
    print("Azure OpenAI Chatbot (type 'exit' to quit)\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        try:
            reply = ask_chat(user_input)
            print("\nBot: " + reply + "\n")
        except Exception as e:
            print("Error calling Azure OpenAI:", str(e))
            try:
                import traceback; traceback.print_exc()
            except:
                pass

if __name__ == "__main__":
    main()
