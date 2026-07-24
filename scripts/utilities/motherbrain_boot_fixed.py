"""
MotherBrain Boot Sequence — Intent-based Dependency Summoning.
"""

import sys
from pathlib import Path

# Add all potential locations to path dynamically
ROOTBASE = Path("/storage/emulated/0/RootBase")
search_paths = [
    ROOTBASE / "src/swarm",
    ROOTBASE / "bleak_core",
    ROOTBASE / "scripts/utilities",
    ROOTBASE / "CodeCity-Bench/src/core",
]

for path in search_paths:
    if path.exists():
        sys.path.insert(0, str(path))

# Now summon by intent
try:
    from motherbrain_governor import MotherBrainGovernor
    print("[+] Governor summoned.")
except ImportError as e:
    print(f"[!] Governor summoning failed: {e}")
    sys.exit(1)

if __name__ == "__main__":
    print("🚀 MOTHERBRAIN BOOT SEQUENCE")
    governor = MotherBrainGovernor()
    governor.run_loop()
