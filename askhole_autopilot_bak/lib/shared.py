from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path("/storage/emulated/0/RootBase/askhole_autopilot")
STATE_DIR = ROOT / "state"
STATE_FILE = STATE_DIR / "autopilot.json"
MRS = Path("/storage/emulated/0/RootBase/mrs_higgins_saas")
VAI = Path("/storage/emulated/0/RootBase/vertical_ai")


def load_json(path: Path, default: Any):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
