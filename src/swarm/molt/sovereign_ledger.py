import hashlib
import json
import time
import os
from pathlib import Path
from datetime import datetime

class ModMindLedger:
    """
    The Immutable ModMind Ledger.
    Creates a cryptographically linked chain of every system action.
    """
    def __init__(self, ledger_path="logs/ModMind_ledger.jsonl"):
        # Convert to Path object for better handling
        self.ledger_path = Path(ledger_path)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        self._last_hash = self._get_last_hash()

    def _get_last_hash(self):
        if not self.ledger_path.exists():
            return "0" * 64
        with open(self.ledger_path, "rb") as f:
            lines = f.readlines()
            if not lines: return "0" * 64
            last_entry = json.loads(lines[-1])
            return last_entry.get("current_hash", "0" * 64)

    def record(self, identity: str, action: str, payload: dict, rationale: str):
        """Records an action with a cryptographic link to the previous entry."""
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        # Create the entry data
        entry_data = {
            "timestamp": timestamp,
            "identity": identity,
            "action": action,
            "payload": payload,
            "rationale": rationale,
            "previous_hash": self._last_hash
        }
        
        # Calculate current hash for immutability
        entry_string = json.dumps(entry_data, sort_keys=True).encode()
        current_hash = hashlib.sha256(entry_string).hexdigest()
        
        entry_data["current_hash"] = current_hash
        self._last_hash = current_hash
        
        with open(self.ledger_path, "a") as f:
            f.write(json.dumps(entry_data) + "
")
            
        return current_hash

# Global instance
ledger = ModMindLedger()
