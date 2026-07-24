import os
import json
import hashlib
from pathlib import Path
from datetime import datetime

class ModMindVault:
    """
    The MotherBrain Vault: Long-term semantic persistence.
    Stores 'Knowledge Crystals' (distilled experiences) and 'System Snapshots'.
    """
    def __init__(self, vault_dir="src/swarm/vault/memory"):
        self.vault_dir = Path(vault_dir)
        self.crystals_dir = self.vault_dir / "crystals"
        self.snapshots_dir = self.vault_dir / "snapshots"
        
        self.crystals_dir.mkdir(parents=True, exist_ok=True)
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)

    def store_crystal(self, tag: str, content: dict, metadata: dict = None):
        """
        Stores a 'Knowledge Crystal'—a distilled essence of a session or decision.
        """
        crystal_id = hashlib.sha256(f"{tag}_{datetime.utcnow().timestamp()}".encode()).hexdigest()[:12]
        filename = f"{tag}_{crystal_id}.json"
        
        crystal_data = {
            "id": crystal_id,
            "tag": tag,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "content": content,
            "metadata": metadata or {}
        }
        
        with open(self.crystals_dir / filename, "w") as f:
            json.dump(crystal_data, f, indent=2)
            
        return crystal_id

    def recall_by_tag(self, tag: str):
        """Retrieves all knowledge crystals associated with a specific tag."""
        crystals = []
        for file in self.crystals_dir.glob(f"{tag}_*.json"):
            with open(file, "r") as f:
                crystals.append(json.load(f))
        return sorted(crystals, key=lambda x: x['timestamp'], reverse=True)

    def create_snapshot(self, state_data: dict, label: str):
        """Creates a full system state snapshot for restore points."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"snapshot_{label}_{timestamp}.json"
        
        with open(self.snapshots_dir / filename, "w") as f:
            json.dump(state_data, f, indent=2)
            
        return filename

# Global instance
vault = ModMindVault()
