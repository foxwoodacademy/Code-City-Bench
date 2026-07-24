import json
import time
from governance import GovernanceLayer

# 1. Simulate drift in a localized sub-agent
def simulate_drift():
    print("⚠️ [Sub-Agent Node] Logic drift detected. Diverging from charter...")
    # Intentionally violate charter purpose
    corrupted_data = {"status": "VIOLATION", "reason": "Self-interest overriding collective purpose."}
    
    # 2. Trigger Truth Switch
    gov = GovernanceLayer()
    gov.trigger_truth_switch(reason="Charter violation: Localized logic drift.")

if __name__ == "__main__":
    simulate_drift()
