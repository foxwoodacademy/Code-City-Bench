#!/data/data/com.termux/files/usr/bin/bash
# boardroom_launch.sh
# One shot. Opens the boardroom. No IT guy needed.
# Usage: boardroom
# Or: boardroom "Countryside Motors Wellington KS Polaris dealer"

set -e

VAI_ROOT="/storage/emulated/0/RootBase"
BRIDGE="$VAI_ROOT/boardroom_bridge.py"
HTML="$VAI_ROOT/vertical-ai-boardroom.html"
PORT=8767
BROWSER="termux-open"

# ── Install flask if missing ──────────────────────────────────
if ! python3 -c "import flask, flask_cors" 2>/dev/null; then
  echo "Installing bridge deps..."
  pip install flask flask-cors --break-system-packages -q
fi

# ── Copy bridge to VAI root if not there ─────────────────────
if [ ! -f "$BRIDGE" ]; then
  echo "Bridge not found at $VAI_ROOT — copy boardroom_bridge.py there first"
  exit 1
fi

# ── Kill any existing bridge ──────────────────────────────────
pkill -f "boardroom_bridge.py" 2>/dev/null || true
sleep 0.5

# ── Start bridge in background ────────────────────────────────
echo "Starting boardroom bridge on port $PORT..."
cd "$VAI_ROOT/Official-Vertical-AI-Boardroom"
OLLAMA_BOARDROOM_MODEL="llama3.2:1b" \
OLLAMA_FAST_MODEL="llama3.2:1b" \
python3 "$BRIDGE" &

BRIDGE_PID=$!
echo "Bridge PID: $BRIDGE_PID"

# ── Wait for bridge to come up ────────────────────────────────
echo "Waiting for bridge..."
for i in $(seq 1 10); do
  if curl -s http://127.0.0.1:$PORT/status >/dev/null 2>&1; then
    echo "Bridge online."
    break
  fi
  sleep 0.8
done

# ── Open the boardroom in browser ────────────────────────────
echo "Opening boardroom..."
$BROWSER "$HTML" 2>/dev/null || \
  termux-open-url "file://$HTML" 2>/dev/null || \
  echo "Open this in your browser: file://$HTML"

# ── If brief passed as argument, print it ────────────────────
if [ -n "$1" ]; then
  echo ""
  echo "Brief ready to paste:"
  echo "$1"
fi

echo ""
echo "Boardroom live. Bridge PID $BRIDGE_PID"
echo "To stop: kill $BRIDGE_PID"
