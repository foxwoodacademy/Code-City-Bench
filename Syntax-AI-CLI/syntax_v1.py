import os
import sys
import json
import google.generativeai as genai
# Import Governance from Implore's shared library path
sys.path.append("/storage/emulated/0/RootBase/Implore/")
from governance import GovernanceLayer

def main():
    # 1. Verification Gate
    gov = GovernanceLayer()
    try:
        gov.verify_charter()
    except Exception as e:
        print(f"FATAL: {e}")
        sys.exit(1)
        
    # 2. Operational Integrity Loop
    if gov.is_integrity_compromised():
        print("🚨 CRITICAL: Truth Switch active. Operations halted.")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)

    # ... rest of operational logic

    # Grab the prompt from the command line arguments
    if len(sys.argv) < 2:
        print("Usage: syntax \"your prompt here\"")
        sys.argv.append(input("Enter prompt: "))

    prompt = " ".join(sys.argv[1:])

    try:
        # Initialize the official client
        client = genai.Client(api_key=api_key)
        
        # Use the standard, reliable gemini-2.5-flash model
        response = client.models.generate_content_stream(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        # Stream the text response directly to the terminal
        for chunk in response:
            print(chunk.text, end="", flush=True)
        print() # New line at the end
        
    except Exception as e:
        print(f"\nAPI Error: {e}")

if __name__ == "__main__":
    main()
