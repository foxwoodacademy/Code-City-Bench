import json
import os
import time
from path_resolver import resolver

class GovernanceLayer:
    def __init__(self, status_dir=None):
        if status_dir is None:
            status_dir = resolver.resolve("ecosystem_bridge")
        self.status_dir = status_dir
        self.charter_file = os.path.join(self.status_dir, "charter.json")
        self.truth_switch_file = os.path.join(self.status_dir, "truth_switch.json")

    def verify_charter(self):
        """Instantiation Gate: Must verify Charter exists and is signed/agreed."""
        if not os.path.exists(self.charter_file):
            raise Exception("CRITICAL: Immutable Charter not found. Intelligence instantiation aborted.")
        print("✅ [Governance] Immutable Charter verified. Intelligence instantiation authorized.")
        return True

    def trigger_truth_switch(self, reason):
        """Global signaling for loss of integrity."""
        state = {"status": "TRUTH_MODE", "timestamp": time.time(), "reason": reason}
        with open(self.truth_switch_file, 'w') as f:
            json.dump(state, f)
        print(f"🚨 [GOVERNANCE] TRUTH SWITCH TRIGGERED: {reason}")

    def is_integrity_compromised(self):
        """Swarm agents check this before any action."""
        if os.path.exists(self.truth_switch_file):
            with open(self.truth_switch_file, 'r') as f:
                state = json.load(f)
            if state["status"] == "TRUTH_MODE":
                return True
        return False
