import os
import json
from pathlib import Path

class ConciergeStateManager:
    """Handles token-aware account rotation and context handoffs."""
    def __init__(self, state_dir="/storage/emulated/0/RootBase/concierge_state"):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.active_state_file = self.state_dir / "current_project_state.json"

    def save_state(self, project_path, phase, stage):
        state = {"project_path": project_path, "phase": phase, "stage": stage}
        with open(self.active_state_file, "w") as f:
            json.dump(state, f)

    def get_handoff_prompt(self):
        with open(self.active_state_file, "r") as f:
            state = json.load(f)
        return f"RESUME CONTEXT: Project '{state['project_path']}', Phase: {state['phase']}, Stage: {state['stage']}. Continue immediately."

class ValetSyncEngine:
    """Synchronizes configurations, aliases, and secrets across environments."""
    def __init__(self, sync_root="/storage/emulated/0/RootBase/valet_sync"):
        self.sync_root = Path(sync_root)
        self.sync_root.mkdir(parents=True, exist_ok=True)

    def push_config(self, config_type, data):
        # Logic to write config to a central synchronized store
        with open(self.sync_root / f"{config_type}.json", "w") as f:
            json.dump(data, f)
            
    def pull_config(self, config_type):
        # Logic to apply config locally
        with open(self.sync_root / f"{config_type}.json", "r") as f:
            return json.load(f)
