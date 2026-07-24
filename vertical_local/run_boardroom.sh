#!/usr/bin/env bash
set -euo pipefail

TMPDIR="${TMPDIR:-/data/data/com.termux/files/usr/tmp}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"
LOG="$TMPDIR/vertical_uvicorn.log"
PIDFILE="$TMPDIR/vertical_uvicorn.pid"

usage(){ echo "Usage: $0 [start|stop|status|install-deps|populate]"; }

CMD="${1:-start}"
case "$CMD" in
  install-deps)
    if [ -f requirements.txt ]; then
      echo "Installing requirements (pip --user)..."
      python3 -m pip install --user -r requirements.txt || { echo "pip install --user failed. Try venv."; exit 1; }
    else
      echo "Installing minimal deps (uvicorn requests)..."
      python3 -m pip install --user uvicorn requests || { echo "pip install --user failed. Try venv."; exit 1; }
    fi
    exit 0
    ;;
  populate)
    if [ -f "$SCRIPT_DIR/../tools/bardildo/populate_persona_map.py" ]; then
      echo "Populating persona_map.json..."
      python3 "$SCRIPT_DIR/../tools/bardildo/populate_persona_map.py" || echo "populate script failed"
    else
      echo "populate_persona_map.py not found at ../tools/bardildo/"
    fi
    exit 0
    ;;
  stop)
    if [ -f "$PIDFILE" ]; then
      PID=$(cat "$PIDFILE")
      echo "Stopping pid $PID"
      kill "$PID" 2>/dev/null || true
      rm -f "$PIDFILE"
      exit 0
    else
      echo "PID file not found"
      exit 1
    fi
    ;;
  status)
    if [ -f "$PIDFILE" ]; then
      PID=$(cat "$PIDFILE")
      if ps -p "$PID" > /dev/null 2>&1; then
        echo "uvicorn running pid $PID; tailing log (last 50 lines):"
        tail -n 50 "$LOG" || true
        exit 0
      else
        echo "PID file present but process not running"
        exit 1
      fi
    else
      echo "Not running"
      exit 1
    fi
    ;;
  start|*)
    ;;
esac

# Ensure tmp dir
mkdir -p "$TMPDIR"

# Quick check for uvicorn; if missing try pip --user
python3 - <<PY
try:
    import uvicorn
except Exception:
    raise SystemExit(2)
else:
    raise SystemExit(0)
PY
RC=$?
if [ "$RC" -eq 2 ]; then
  echo "uvicorn not found. Attempting pip install (--user)..."
  python3 -m pip install --user uvicorn requests || echo "pip install failed; ensure dependencies are available or run $0 install-deps"
fi

# Start server
echo "Starting uvicorn on $HOST:$PORT (logs -> $LOG)"
nohup python3 -m uvicorn app:app --host "$HOST" --port "$PORT" > "$LOG" 2>&1 &
echo $! > "$PIDFILE"
echo "Started. PID=$(cat $PIDFILE)"
echo "Open: http://$HOST:$PORT/boardroom"

exit 0
