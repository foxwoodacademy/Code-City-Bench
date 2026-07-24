#!/usr/bin/env python3
"""
CodeMentor MVP - Extraction Verification
Run this to confirm the extraction worked correctly.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

def verify():
    errors = []

    try:
        from core.six_hats import SixHatsEngine, HatPrompt
        engine = SixHatsEngine()
        hats = engine.get_all_hats()
        assert len(hats) == 6
        print(f"✅ SixHatsEngine: {len(hats)} hats loaded")
    except Exception as e:
        errors.append(f"❌ SixHatsEngine: {e}")

    try:
        from core.state_engine import StateEngine
        state = StateEngine(data_dir="/tmp/codementor_test")
        dashboard = state.get_dashboard_data()
        assert "global_level" in dashboard
        print(f"✅ StateEngine: initialized, level {dashboard['global_level']}")
    except Exception as e:
        errors.append(f"❌ StateEngine: {e}")

    try:
        from core.progression_engine import ProgressionEngine
        print("✅ ProgressionEngine: imported")
    except Exception as e:
        errors.append(f"❌ ProgressionEngine: {e}")

    try:
        from bridge.api_bridge import APIBridge
        bridge = APIBridge()
        print(f"✅ APIBridge: initialized, backend={bridge.active_backend}")
    except Exception as e:
        errors.append(f"❌ APIBridge: {e}")

    print()
    if errors:
        print("ERRORS:")
        for e in errors:
            print(f"  {e}")
        return False
    else:
        print("🎉 All systems nominal. CodeMentor MVP is extracted and runnable.")
        return True

if __name__ == "__main__":
    ok = verify()
    sys.exit(0 if ok else 1)
