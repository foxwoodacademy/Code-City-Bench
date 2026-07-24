import os
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from src.tools.tools import scrape_web_data, search_tool

# --- CONFIG ---
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "PASTE_YOUR_KEY_HERE")

# Researcher: Fast, local (Ollama)
researcher_llm = ChatOllama(model="llama3.1", temperature=0)

# Strategy Agent: High-reasoning (Gemini)
strategy_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

def researcher_agent(client_name, focus):
    print(f"\n[RESEARCHER] Scanning for data on {client_name}...")
    query = f"{focus} {client_name}"
    
    search_res = search_tool.invoke({"query": query})
    lines = search_res.split("\n")
    if not lines or ": " not in lines[0]:
        return "No relevant search results found."
        
    url = lines[0].split(": ")[1]
    print(f"[RESEARCHER] Reading: {url}")
    data = scrape_web_data.invoke({"url": url})
    return f"Data from {url}:\n{data[:2000]}"

def strategy_agent(client_name, data):
    print(f"[STRATEGY] Synthesizing report for {client_name}...")
    prompt = f"You are a Senior Auditor. Synthesize this data into a professional risk brief:\n{data}"
    return strategy_llm.invoke(prompt).content

if __name__ == "__main__":
    print("\n[SYSTEM] Hybrid Swarm Initialized.")
    
    clients = [{"name": "Bank of England", "focus": "Base Rate May 2026"}]

    for client in clients:
        raw_data = researcher_agent(client['name'], client['focus'])
        report = strategy_agent(client['name'], raw_data)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"src/data/report_{client['name'].replace(' ', '_')}_{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[SUCCESS] Report saved to {filename}")
