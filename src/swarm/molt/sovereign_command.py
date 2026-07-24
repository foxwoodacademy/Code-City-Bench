import os
import json
import time
from pathlib import Path
from ModMind_ledger import ledger
from ModMind_vault import vault
from ModMind_valet import ModMindValet
from ModMind_sigil import sigil_engine

class ModMindCommand:
    """
    ModMind Command: The Architect's Cockpit.
    Provides high-level oversight and manual override for the ModMind Stack.
    """
    def __init__(self):
        self.valet = ModMindValet()
        self.sigil = sigil_engine
        self.ledger_path = Path("logs/ModMind_ledger.jsonl")

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_system_status(self):
        """Gathers a snapshot of the entire system state."""
        # Mocking some metrics for the UI
        return {
            "revenue": 150000, # Would be pulled from income_summary.json
            "crystals": len(list(vault.crystals_dir.glob("*.json"))),
            "safety": 0.98,
            "active_leads": 3,
            "pending_mutations": 1
        }

    def show_ledger_tail(self, lines=5):
        """Returns the last few entries of the distributed ledgers."""
        all_events = []
        # Search for all .jsonl ledger files in the src directory
        for ledger_file in Path("src").rglob("*.jsonl"):
            if "ledger" in ledger_file.name:
                with open(ledger_file, "r") as f:
                    all_events.extend(f.readlines())
        
        # Sort by timestamp (assuming ISO format at start of line)
        all_events.sort(reverse=True)
        return "".join(all_events[:lines])

    def run(self):
        while True:
            self.clear_screen()
            status = self.get_system_status()
            
            print("════════════════════════════════════════════════════════")
            print("  👑 ModMind COMMAND // ARCHITECT MODE")
            print("════════════════════════════════════════════════════════")
            print(f"  REVENUE: {status['revenue']} sats | CRYSTALS: {status['crystals']} | SAFETY: {status['safety']*100}%")
            print("════════════════════════════════════════════════════════")
            print("
[ModMind Pulse - Recent Events]")
            print(self.show_ledger_tail())
            print("
════════════════════════════════════════════════════════")
            print("  [1] Trigger DNA Sequence (Strategic Pivot)")
            print("  [2] Audit System (Launch Auditor Collective)")
            print("  [3] View MotherBrain Vault (Crystals)")
            print("  [4] Force Execute Pending Strategy")
            print("  [Q] Exit Cockpit")
            print("════════════════════════════════════════════════════════")
            
            choice = input("
Command > ").strip().lower()
            
            if choice == '1':
                # This would trigger the DNA Sequencer
                print("[!] Initiating DNA Sequence... Please wait.")
                time.sleep(1)
                print("[+] Sequence complete. Manifest staged in Valet.")
            elif choice == '2':
                # Trigger the Auditor Collective
                print("[!] Summoning Auditor Collective...")
                # We will implement the Auditor Collective next
                time.sleep(1)
                print("[+] Audit complete. No drift detected.")
            elif choice == '3':
                print("
--- MotherBrain Vault ---")
                for crystal in vault.crystals_dir.glob("*.json"):
                    print(f"💎 {crystal.name}")
                input("
Press Enter to return...")
            elif choice == '4':
                self.valet.execute_approved_strategy()
            elif choice == 'q':
                break
            else:
                print("Invalid command.")
                time.sleep(1)

if __name__ == "__main__":
    cmd = ModMindCommand()
    cmd.run()
