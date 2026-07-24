from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

BASE_OUTBOUND = Path("/storage/emulated/0/RootBase/New-SaaS/data_outbound")
DEFAULT_NODES = ("boardroom", "hotseat", "askhole", "scouts")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_outbound_tree(base_dir: Path = BASE_OUTBOUND, nodes: Iterable[str] = DEFAULT_NODES) -> Path:
    base_dir.mkdir(parents=True, exist_ok=True)
    for node in nodes:
        (base_dir / node).mkdir(parents=True, exist_ok=True)
    return base_dir


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, content: str, append: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if append else "w"
    with path.open(mode, encoding="utf-8") as fh:
        fh.write(content)
