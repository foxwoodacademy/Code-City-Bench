import os
import sys
import requests
import json

# Minimalist Router
# Usage: python3 smart_router.py "your prompt"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def route_request(prompt):
    # 1. Classification (Simulated Tiny Logic)
    # If it's a short question, answer locally. If complex, route to Groq.
    if len(prompt) < 50:
        return "local"
    return "groq"

def call_groq(prompt):
    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY not set."
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content']

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 smart_router.py 'your prompt'")
        return
    
    prompt = sys.argv[1]
    destination = route_request(prompt)
    
    if destination == "local":
        print("--- Local Route (Tiny Model) ---")
        print("Simulated tiny model response: Your request was simple and handled locally.")
    else:
        print("--- Groq Route (Cloud Intelligence) ---")
        print(call_groq(prompt))

if __name__ == "__main__":
    main()
