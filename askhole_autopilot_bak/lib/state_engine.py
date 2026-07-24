from __future__ import annotations

import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from shared import STATE_FILE, load_json, save_json

class State:
    def __init__(self):
        self.data = {
            "mode": "IDLE",
            "triggers": [],
            "invoices": 0,
            "settled": 0,
            "copy": 0,
            "last_action": None
        }
        self.load()

    def load(self):
        self.data.update(load_json(STATE_FILE, {}))

    def save(self):
        save_json(STATE_FILE, self.data)

    def trigger(self, event, payload=None):
        self.data["triggers"].append({
            "ts": time.time(),
            "event": event,
            "payload": payload
        })
        self.data["triggers"] = self.data["triggers"][-100:]
        self.data["last_action"] = event
        self.save()

    def mode(self, m):
        self.data["mode"] = m
        self.save()

STATE = State()
