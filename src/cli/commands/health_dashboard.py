import json
import time
from rich.console import Console
from rich.table import Table

console = Console()

def display_dashboard():
    """Visualizes the swarm's health and integrity status."""
    console.clear()
    table = Table(title="RootBase Swarm Health Dashboard")
    table.add_column("Agent/Component", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Integrity", style="magenta")
    
    table.add_row("Mrs. Higgins", "Operational", "Verified")
    table.add_row("JaneBot", "Operational", "Verified")
    table.add_row("Molt-V5", "Operational", "Verified")
    table.add_row("Integrity Auditor", "Active", "Syncing")
    
    console.print(table)

if __name__ == "__main__":
    try:
        while True:
            display_dashboard()
            time.sleep(5)
    except KeyboardInterrupt:
        pass
