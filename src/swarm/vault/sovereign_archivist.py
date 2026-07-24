import os
import json
from pathlib import Path
from ModMind_vault import vault
from concierge import concierge

class ModMindArchivist:
    """
    The ModMind Archivist: The 'Librarian' of the system.
    Distills raw session logs into structured Knowledge Crystals.
    """
    def __init__(self, log_dir="logs"):
        self.log_dir = Path(log_dir)

    def distill_session(self, log_file: str, tag: str = "session_summary"):
        """
        Reads a session log, uses the Concierge to distill the 'essence', 
        and stores it in the Vault.
        """
        log_path = self.log_dir / log_file
        if not log_path.exists():
            return None

        print(f"[Archivist] Distilling session {log_file} into a Knowledge Crystal...")
        
        # Read the log (truncated if too large)
        with open(log_path, "r") as f:
            content = f.read()
            if len(content) > 10000:
                content = content[-10000:] # Focus on the resolution/ending

        # Use the Concierge to summarize the 'Win' or 'Loss'
        summary, err = concierge.generate(
            prompt=f"Analyze this session log and extract the 'Knowledge Crystal'. 

Log:
{content}

Extract: 1. The Core Problem, 2. The Solution that worked, 3. The Lesson learned for future iterations.",
            system="You are the ModMind Archivist. Distill raw logs into high-density strategic knowledge."
        )
        
        if err:
            print(f"[-] Distillation failed: {err}")
            return None

        # Structure the distillation
        distillation = {
            "summary": summary,
            "type": "experience",
            "impact": "high" if "success" in summary.lower() else "medium"
        }
        
        crystal_id = vault.store_crystal(tag, distillation, {"source_log": log_file})
        print(f"[+] Crystal created: {crystal_id}")
        return crystal_id

if __name__ == "__main__":
    # Example: Distill the latest oneshot log
    archivist = ModMindArchivist()
    # Find the latest log file in logs/
    logs = sorted(Path("logs").glob("oneshot_*.log"))
    if logs:
        archivist.distill_session(logs[-1].name, tag="revenue_pipeline")
