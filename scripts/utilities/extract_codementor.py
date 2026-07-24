#!/usr/bin/env python3
"""
CodeMentor Extraction Script
Pulls the generator-style source files into a clean, runnable directory structure.
Run this once from /storage/emulated/0/RootBase/
"""

import os
import re
from pathlib import Path

BASE_DIR = Path("/storage/emulated/0/RootBase/Kimi-CodeMentor-MVP")
OUT_DIR = Path("/storage/emulated/0/RootBase/codementor_extracted")

# Directory structure to create
DIRS = [
    "core",
    "tiers",
    "challenges",
    "data",
    "bridge",
]

def extract_python_string(filepath: Path) -> str:
    """
    Pull the actual Python code out of generator-style files.
    Handles both:
    - Files that are plain Python (just read them)
    - Files where code is in a triple-quoted string variable (extract it)
    """
    content = filepath.read_text(errors="ignore")

    # Check if it's a generator file (has a string assignment like six_hats_py = '''...)
    match = re.search(r"(?:[\w_]+_py)\s*=\s*['\"{3}]{3}(.*?)['\"{3}]{3}", content, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Plain Python file - return as-is but strip the write-to-disk lines at the bottom
    lines = content.split("\n")
    clean = []
    for line in lines:
        # Stop at the file-writing block
        if line.strip().startswith("with open(") and "write(" in "".join(lines[lines.index(line):lines.index(line)+3]):
            break
        clean.append(line)
    return "\n".join(clean).strip()


def setup_dirs():
    for d in DIRS:
        (OUT_DIR / d).mkdir(parents=True, exist_ok=True)
    # Init files
    for d in DIRS:
        init = OUT_DIR / d / "__init__.py"
        if not init.exists():
            init.write_text("# CodeMentor package\n")
    (OUT_DIR / "__init__.py").write_text("# CodeMentor root\n")
    print(f"✅ Directory structure created at {OUT_DIR}")


def extract_files():
    file_map = {
        "six_hats.py":          OUT_DIR / "core" / "six_hats.py",
        "state_engine.py":      OUT_DIR / "core" / "state_engine.py",
        "progression_engine.py":OUT_DIR / "core" / "progression_engine.py",
        "skill_tree.py":        OUT_DIR / "core" / "skill_tree.py",
        "challenge_generator.py":OUT_DIR / "challenges" / "challenge_generator.py",
        "kimi_code.py":         OUT_DIR / "bridge" / "kimi_code.py",
        "api_bridge.py":        OUT_DIR / "bridge" / "api_bridge.py",
    }

    for src_name, dest_path in file_map.items():
        src = BASE_DIR / src_name
        if src.exists():
            code = extract_python_string(src)
            dest_path.write_text(code + "\n")
            print(f"✅ Extracted: {src_name} → {dest_path.relative_to(OUT_DIR)}")
        else:
            print(f"⚠️  Not found: {src_name} (skipping)")

    # Tier files from Kimi or wherever they landed
    tier_sources = {
        "novice.py":     OUT_DIR / "tiers" / "novice.py",
        "apprentice.py": OUT_DIR / "tiers" / "apprentice.py",
        "journeyman.py": OUT_DIR / "tiers" / "journeyman.py",
        "expert.py":     OUT_DIR / "tiers" / "expert.py",
        "master.py":     OUT_DIR / "tiers" / "master.py",
        "architect.py":  OUT_DIR / "tiers" / "architect.py",
    }

    # Search both dirs
    search_dirs = [BASE_DIR, Path("/storage/emulated/0/RootBase/Kimi-Code-v1.0-Fixed")]
    for src_name, dest_path in tier_sources.items():
        found = False
        for search in search_dirs:
            src = search / src_name
            if src.exists():
                code = extract_python_string(src)
                dest_path.write_text(code + "\n")
                print(f"✅ Extracted tier: {src_name}")
                found = True
                break
        if not found:
            print(f"⚠️  Tier not found: {src_name}")


def write_main():
    """Write a simple main.py to verify the extraction worked."""
    main = OUT_DIR / "main.py"
    main.write_text('''#!/usr/bin/env python3
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
''')
    print("✅ main.py written")


if __name__ == "__main__":
    print("CodeMentor Extraction Script")
    print("=" * 40)
    setup_dirs()
    extract_files()
    write_main()
    print()
    print("=" * 40)
    print(f"Done. Run: python3 {OUT_DIR}/main.py to verify.")
