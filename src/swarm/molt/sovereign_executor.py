import os
import json
import shutil
from pathlib import Path
from datetime import datetime

class ModMindExecutor:
    """
    The ModMind Executor: The 'Hand' of the system.
    Performs surgical updates to the codebase based on Developer Manifests.
    """
    def __init__(self, backup_dir="logs/deploy_backups"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def _create_backup(self, file_path: Path):
        """Creates a timestamped backup of a file before mutation."""
        if not file_path.exists():
            return None
        
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"{file_path.name}_{timestamp}.bak"
        shutil.copy2(file_path, backup_path)
        return backup_path

    def apply_manifest(self, manifest: dict):
        """
        Surgically applies the changes proposed in a Developer Manifest.
        """
        target_package = manifest.get("target_package")
        proposed_changes = manifest.get("proposed_changes")
        
        if not target_package or not proposed_changes:
            return {"status": "error", "message": "Invalid manifest: missing target or changes."}

        # Path to the package JSON
        package_path = Path(f"src/saas/higgins/saas_packages/{target_package}.json")
        
        try:
            # 1. Backup first
            backup = self._create_backup(package_path)
            
            # 2. Read current state
            if package_path.exists():
                with open(package_path, "r") as f:
                    data = json.load(f)
            else:
                data = {"name": target_package}

            # 3. Apply changes (This is a simplified version; 
            # in production, this would use a more sophisticated merge logic)
            # For now, we assume the proposed_changes is a JSON-compatible update
            try:
                updates = json.loads(proposed_changes)
                data.update(updates)
            except json.JSONDecodeError:
                # If it's just text, we add it to a 'description' or 'notes' field
                data["strategic_pivot"] = proposed_changes
                data["last_mutation"] = datetime.utcnow().isoformat() + "Z"

            # 4. Write back to disk
            with open(package_path, "w") as f:
                json.dump(data, f, indent=2)

            return {
                "status": "success", 
                "backup": str(backup), 
                "target": str(package_path)
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

# Global instance
executor = ModMindExecutor()
