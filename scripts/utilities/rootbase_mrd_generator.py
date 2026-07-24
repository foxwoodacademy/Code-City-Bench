import os
import requests
import json
from pathlib import Path

# --- Configuration ---
OLLAMA_HOST = "http://127.0.0.1:11434"
MODEL = "deepseek-r1:1.5b" # Using the lightweight R1 for fast scanning
ROOT_DIR = Path("/storage/emulated/0/RootBase")

def query_ollama(prompt):
    try:
        resp = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={"model": MODEL, "prompt": prompt, "stream": False},
            timeout=60
        )
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except Exception as e:
        return f"Error querying Ollama: {e}"

def generate_mrd(folder_path):
    # Gather context about the folder
    files = [f.name for f in folder_path.iterdir() if f.is_file()]
    subdirs = [d.name for d in folder_path.iterdir() if d.is_dir()]
    
    context = f"Folder: {folder_path}
Files: {files}
Subdirectories: {subdirs}"
    
    prompt = f"""
    You are a senior technical architect. I have a folder in a high-autonomy agentic stack called RootBase.
    The folder is missing a README.md. Based on the following contents, write a concise 'Market Requirements Document' (MRD.txt).
    
    The MRD should include:
    1. Purpose: What is this module's core function?
    2. Target: Who or what is this designed for?
    3. Core Logic: What are the primary scripts or logic flows?
    4. Value Proposition: Why does this exist in a revenue-generative pipeline?

    CONTEXT:
    {context}
    
    Return ONLY the text for the MRD.txt file. No conversational filler.
    """
    
    print(f"[+] Generating MRD for {folder_path}...")
    return query_ollama(prompt)

def main():
    print(f"🚀 Starting RootBase MRD Auto-Generator (Model: {MODEL})...")
    
    # Walk through the root directory
    for root, dirs, files in os.walk(ROOT_DIR):
        root_path = Path(root)
        
        # Skip hidden directories (like .git)
        if any(part.startswith('.') for part in root_path.parts):
            continue
            
        # Check if README.md exists
        if "README.md" not in files:
            # Only generate for folders that actually have content (don't document empty folders)
            if files or dirs:
                mrd_content = generate_mrd(root_path)
                mrd_file = root_path / "MRD.txt"
                
                with open(mrd_file, "w") as f:
                    f.write(mrd_content)
                print(f" ✅ Created {mrd_file}")

if __name__ == "__main__":
    main()
