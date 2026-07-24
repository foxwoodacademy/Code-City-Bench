#!/bin/bash
set -e
BASE="/storage/emulated/0/RootBase/askhole_autopilot"
mkdir -p "$BASE"/{bin,lib,state,webhooks,triggers}

# ── lib/state_engine.py ──────────────────────────────────────────────────────
cat > "$BASE/lib/state_engine.py" << 'PYEOF'
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
PYEOF

# ── lib/pipeline.py ──────────────────────────────────────────────────────────
cat > "$BASE/lib/pipeline.py" << 'PYEOF'
import subprocess, sys, os
sys.path.insert(0, "/storage/emulated/0/RootBase/askhole_autopilot/lib")
from state_engine import State

MRS = "/storage/emulated/0/RootBase/mrs_higgins_saas"
VAI = "/storage/emulated/0/RootBase/vertical_ai"

def run(cmd, cwd=MRS, timeout=300):
    try:
        r = subprocess.run(
            cmd, shell=True, capture_output=True,
            text=True, timeout=timeout, cwd=cwd
        )
        State().trigger("exec", {
            "cmd": cmd,
            "rc": r.returncode,
            "out": r.stdout[:500]
        })
        return r
    except Exception as e:
        State().trigger("error", {"cmd": cmd, "err": str(e)})
        return None

def pipeline(dry=False, platform=None):
    c = f"bash {MRS}/mrs_higgins.sh"
    if dry:      c += " --dry-run"
    if platform: c += f" --platform {platform}"
    return run(c)

def bookkeeper():
    return run(f"python3 {MRS}/bookkeeper.py")

def copywriter(pkg, platform):
    return run(f"python3 {MRS}/copywriter.py --package {pkg} --platform {platform}")

def scout(target):
    return run(f"python3 {VAI}/scouts/swarm_intel.py --query {target}", cwd=VAI)
PYEOF

# ── bin/askhole-daemon ───────────────────────────────────────────────────────
cat > "$BASE/bin/askhole-daemon" << 'PYEOF'
#!/usr/bin/env python3
import sys, os, time, json, signal
sys.path.insert(0, "/storage/emulated/0/RootBase/askhole_autopilot/lib")
from pipeline import pipeline, bookkeeper, copywriter, scout
from state_engine import State

PIDFILE = "/storage/emulated/0/RootBase/askhole_autopilot/state/daemon.pid"

def daemonize():
    # Termux-safe double-fork
    if os.fork(): sys.exit(0)
    os.setsid()
    if os.fork(): sys.exit(0)
    with open(PIDFILE, 'w') as f:
        f.write(str(os.getpid()))

def handle(sig, frame):
    State().trigger("shutdown", {"signal": sig})
    if os.path.exists(PIDFILE):
        os.remove(PIDFILE)
    sys.exit(0)

signal.signal(signal.SIGTERM, handle)
signal.signal(signal.SIGINT,  handle)

def main():
    daemonize()
    S = State()
    S.trigger("boot")
    while True:
        S.load()  # re-read state each tick so external triggers take effect
        mode = S.data.get("mode", "IDLE")

        if mode == "SHIP":
            S.trigger("pipeline_start")
            pipeline(dry=False)
            bookkeeper()
            S.data["mode"] = "MONITOR"
            S.save()

        elif mode == "GENERATE":
            for p in ["Fiverr", "Upwork", "Nostr", "Reddit", "ProductHunt"]:
                copywriter("askhole.json", p)
            S.data["copy"] += 5
            S.data["mode"] = "IDLE"
            S.save()

        elif mode == "SCOUT":
            scout("askhole")
            S.data["mode"] = "IDLE"
            S.save()

        time.sleep(30)

if __name__ == "__main__":
    main()
PYEOF
chmod +x "$BASE/bin/askhole-daemon"

# ── bin/askhole-trigger ──────────────────────────────────────────────────────
cat > "$BASE/bin/askhole-trigger" << 'PYEOF'
#!/usr/bin/env python3
import sys, json
sys.path.insert(0, "/storage/emulated/0/RootBase/askhole_autopilot/lib")
from state_engine import State

if len(sys.argv) < 2:
    print("Usage: askhole-trigger <event> [payload_json]")
    sys.exit(1)

S = State()
payload = json.loads(sys.argv[2]) if len(sys.argv) > 2 else None
S.trigger(sys.argv[1], payload)

MODE_MAP = {
    "mode_ship":     "SHIP",
    "mode_generate": "GENERATE",
    "mode_scout":    "SCOUT",
    "mode_monitor":  "MONITOR",
    "mode_idle":     "IDLE",
}
if sys.argv[1] in MODE_MAP:
    S.data["mode"] = MODE_MAP[sys.argv[1]]
    S.save()

print(f"Triggered: {sys.argv[1]}  |  Mode: {S.data['mode']}")
PYEOF
chmod +x "$BASE/bin/askhole-trigger"

# ── bin/askhole-status ───────────────────────────────────────────────────────
cat > "$BASE/bin/askhole-status" << 'PYEOF'
#!/usr/bin/env python3
import sys, json
sys.path.insert(0, "/storage/emulated/0/RootBase/askhole_autopilot/lib")
from state_engine import State

S = State()
print(json.dumps(S.data, indent=2))
PYEOF
chmod +x "$BASE/bin/askhole-status"

# ── bin/askhole-webhook ──────────────────────────────────────────────────────
cat > "$BASE/bin/askhole-webhook" << 'PYEOF'
#!/usr/bin/env python3
import http.server, socketserver, json, sys
sys.path.insert(0, "/storage/emulated/0/RootBase/askhole_autopilot/lib")
from state_engine import State

PORT = 8765

class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/trigger":
            length = int(self.headers.get('Content-Length', 0))
            body   = self.rfile.read(length)
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self.send_response(400); self.end_headers()
                self.wfile.write(b'{"error":"bad json"}')
                return
            S = State()
            S.trigger(data.get("event"), data.get("payload"))
            if data.get("mode"):
                S.data["mode"] = data["mode"]
                S.save()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            self.send_response(404); self.end_headers()

    def log_message(self, format, *args):
        pass  # silent

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"Webhook listening on :{PORT}")
    httpd.serve_forever()
PYEOF
chmod +x "$BASE/bin/askhole-webhook"

# ── triggers/ (Termux widget shortcuts) ─────────────────────────────────────
cat > "$BASE/triggers/ship.sh" << 'EOF'
#!/bin/bash
/storage/emulated/0/RootBase/askhole_autopilot/bin/askhole-trigger mode_ship
EOF
chmod +x "$BASE/triggers/ship.sh"

cat > "$BASE/triggers/generate.sh" << 'EOF'
#!/bin/bash
/storage/emulated/0/RootBase/askhole_autopilot/bin/askhole-trigger mode_generate
EOF
chmod +x "$BASE/triggers/generate.sh"

cat > "$BASE/triggers/scout.sh" << 'EOF'
#!/bin/bash
/storage/emulated/0/RootBase/askhole_autopilot/bin/askhole-trigger mode_scout
EOF
chmod +x "$BASE/triggers/scout.sh"

cat > "$BASE/triggers/idle.sh" << 'EOF'
#!/bin/bash
/storage/emulated/0/RootBase/askhole_autopilot/bin/askhole-trigger mode_idle
EOF
chmod +x "$BASE/triggers/idle.sh"

cat > "$BASE/triggers/status.sh" << 'EOF'
#!/bin/bash
/storage/emulated/0/RootBase/askhole_autopilot/bin/askhole-status
EOF
chmod +x "$BASE/triggers/status.sh"

# ── Verify ───────────────────────────────────────────────────────────────────
echo ""
echo "=== askhole_autopilot install complete ==="
find "$BASE" -type f | sort
echo ""
echo "Quick test:"
echo "  $BASE/bin/askhole-status"
echo "  $BASE/bin/askhole-trigger mode_ship"
echo "  $BASE/bin/askhole-daemon   # starts background loop"
echo "  $BASE/bin/askhole-webhook  # starts HTTP trigger server on :8765"
