import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from ModMind_vault import vault
from ModMind_ledger import ledger

class ModMindOptimizer:
    """
    The ModMind Optimizer: The 'CFO' of the RootBase ecosystem.
    Correlates revenue to DNA mutations and triggers recursive pivots.
    """
    def __init__(self, income_file="logs/income_summary.json"):
        self.income_file = Path(income_file)
        self.ledger_file = Path("logs/ModMind_ledger.jsonl")

    def _get_recent_revenue(self, days=7):
        """Parses the income summary for recent payments."""
        if not self.income_file.exists():
            return []
        
        with open(self.income_file, "r") as f:
            data = json.load(f)
            
        # Assuming income_summary.json is a list of payments or a dict with a 'payments' list
        payments = data.get("payments", []) if isinstance(data, dict) else []
        
        # Filter by timestamp
        cutoff = datetime.utcnow() - timedelta(days=days)
        recent_payments = [
            p for p in payments 
            if datetime.fromisoformat(p['timestamp'].replace("Z", "")) > cutoff
        ]
        return recent_payments

    def correlate_revenue_to_dna(self, payment):
        """
        Matches a payment to the specific mutation that caused it.
        Searches the ModMindLedger for the most recent STRATEGY_EXECUTED event 
        for the package associated with the payment.
        """
        payment_id = payment.get("payment_id")
        package_name = payment.get("package")
        
        if not package_name:
            return None

        # Scan the ledger backwards to find the last deployment for this package
        with open(self.ledger_file, "r") as f:
            lines = f.readlines()
            for line in reversed(lines):
                entry = json.loads(line)
                if entry["action"] == "STRATEGY_EXECUTED" and 
                   entry["payload"].get("target") and package_name in entry["payload"]["target"]:
                    return entry # This is the 'Winning DNA'
        
        return None

    def evaluate_performance(self, package_name):
        """
        Determines if a package is 'Winning' or 'Stalling'.
        """
        payments = self._get_recent_revenue()
        package_payments = [p for p in payments if p.get("package") == package_name]
        
        revenue_total = sum(p.get("amount", 0) for p in package_payments)
        conversion_rate = len(package_payments) # Simplified: total payments as a proxy
        
        # Define thresholds for 'Winning' and 'Stalling'
        if revenue_total > 100000: # Example: 100k sats
            return "WINNING", revenue_total
        elif len(package_payments) == 0:
            return "STALLING", 0
        else:
            return "STABLE", revenue_total

    def optimize(self, valet=None):
        """
        The main optimization loop.
        1. Identify winners -> Crystallize DNA.
        2. Identify stallers -> Trigger Pivot.
        """
        print("[Optimizer] Analyzing revenue-to-DNA correlation...")
        
        # Get all current packages from the filesystem
        packages_dir = Path("src/saas/higgins/saas_packages")
        if not packages_dir.exists():
            return
            
        for pkg_file in packages_dir.glob("*.json"):
            pkg_name = pkg_file.stem
            status, value = self.evaluate_performance(pkg_name)
            
            if status == "WINNING":
                print(f"[+] Package {pkg_name} is WINNING ({value} sats). Crystallizing DNA...")
                winning_dna = self.correlate_revenue_to_dna({"package": pkg_name})
                if winning_dna:
                    vault.store_crystal(
                        tag=f"winner_{pkg_name}",
                        content={
                            "strategy": winning_dna["payload"],
                            "revenue": value,
                            "timestamp": winning_dna["timestamp"]
                        },
                        metadata={"outcome": "high_conversion"}
                    )
            
            elif status == "STALLING" and valet:
                print(f"[!] Package {pkg_name} is STALLING. Triggering Strategic Pivot...")
                # Trigger the Valet to re-run the intelligence loop for this package
                valet.orchestrate_insight({"package": pkg_name, "content_snippet": "Underperforming: Zero revenue in last 7 days."})

# Global instance
optimizer = ModMindOptimizer()
