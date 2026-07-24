import os
import click
from dotenv import load_dotenv
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from src.tools.tools import scrape_web_data, search_tool
from commands.godmode import godmode
from commands.internal_visibility import dev, superdebug

# Load credentials from .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

@click.group()
def cli():
    """Main CLI Entry Point."""
    pass

# Register commands
cli.add_command(godmode)
cli.add_command(dev)
cli.add_command(superdebug)

# ... [rest of the researcher/strategy agent logic]
@cli.command()
def run_swarm():
    """Run the Hybrid Swarm."""
    print("\n[SYSTEM] Hybrid Swarm Initialized.")
    # ... [rest of original main logic]
    clients = [{"name": "Bank of England", "focus": "Base Rate May 2026"}]

    for client in clients:
        raw_data = researcher_agent(client['name'], client['focus'])
        report = strategy_agent(client['name'], raw_data)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        os.makedirs("src/data", exist_ok=True)
        filename = f"src/data/report_{client['name'].replace(' ', '_')}_{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[SUCCESS] Report saved to {filename}")

if __name__ == "__main__":
    cli()
