import json, os, time
from pathlib import Path
STATE_FILE = Path("/storage/emulated/0/RootBase/askhole_autopilot/state/autopilot.json")

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
        if STATE_FILE.exists():
            with open(STATE_FILE) as f:
                self.data.update(json.load(f))

    def save(self):
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)

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
