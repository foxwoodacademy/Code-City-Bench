"""Append-only JSONL store for datacampus records."""

import json
import time
from dataclasses import asdict, is_dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STORE = PROJECT_ROOT / "datacampus_records.jsonl"


def append_record(record_type, payload, store_path=None):
    """Append one record to the store."""
    if store_path is None:
        store_path = DEFAULT_STORE
    if is_dataclass(payload):
        payload = asdict(payload)
    record = {
        "record_type": record_type,
        "created_at": time.time(),
        "payload": payload,
    }
    with Path(store_path).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    return record


def read_records(store_path=None):
    """Read all records from the store."""
    if store_path is None:
        store_path = DEFAULT_STORE
    path = Path(store_path)
    if not path.exists():
        return []
    records = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def latest_payload(record_type, key, value, store_path=None):
    """Return the latest payload matching a key/value pair."""
    if store_path is None:
        store_path = DEFAULT_STORE
    for record in reversed(read_records(store_path)):
        payload = record.get("payload", {})
        if record.get("record_type") == record_type and payload.get(key) == value:
            return payload
    return None
