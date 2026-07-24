#!/usr/bin/env bash
# Create an advanced Termux widget script that ensures a fully operational environment.
# Usage: bash create_improved_widget.sh /path/to/RootBase/vertical_local

REPO_DIR="${1:-/storage/emulated/0/RootBase/vertical_local}"
SHORTCUT_DIR="$HOME/.shortcuts"
WIDGET_SCRIPT="$SHORTCUT_DIR/vertical_boardroom_widget.sh"

mkdir -p "$SHORTCUT_DIR"

cat > "$WIDGET_SCRIPT" <<'SH'
#!/bin/bash
# Advanced Smart-Start/Stop for Vertical AI Boardroom
REPO_DIR="__REPO_DIR__"
SCRIPT="$REPO_DIR/run_boardroom.sh"
PIDFILE="${TMPDIR:-/data/data/com.termux/files/usr/tmp}/vertical_uvicorn.pid"
HOST="127.0.0.1"
PORT="8000"

# Check if server is running
if [ -f "$PIDFILE" ]; then
  PID=$(cat "$PIDFILE" 2>/dev/null || true)
  if [ -n "$PID" ] && ps -p "$PID" > /dev/null 2>&1; then
    # Server is running. For a widget, we'll just show status and ask to stop.
    echo "--- Vertical AI Status ---"
    echo "Server is ACTIVE (PID: $PID)"
    echo "URL: http://$HOST:$PORT/boardroom"
    echo ""
    echo "1) Stop Server"
    echo "2) Cancel"
    read -p "Select an option: " choice
    case "$choice" in
      1) 
        echo "Stopping server..."
        bash "$SCRIPT" stop
        echo "Stopped."
        ;;
      *)
        echo "Operation cancelled."
        ;;
    esac
    exit 0
  fi
fi

# If we reach here, server is NOT running. Let's prepare and start.
echo "--- Initializing Vertical AI Boardroom ---"

echo "[1/3] Checking dependencies..."
bash "$SCRIPT" install-deps

echo "[2/3] Ensuring personas are populated..."
bash "$SCRIPT" populate

echo "[3/3] Starting the engine..."
bash "$SCRIPT" start

if [ $? -eq 0 ]; then
  echo "----------------------------------------"
  echo "SUCCESS: Boardroom is live!"
  echo "URL: http://$HOST:$PORT/boardroom"
  echo "----------------------------------------"
  # Attempt to open the browser automatically
  termux-open "http://$HOST:$PORT/boardroom"
else
  echo "FAILED: Could not start the engine. Check logs."
fi

exit 0
SH

# Replace placeholder with actual path
sed -i "s#__REPO_DIR__#${REPO_DIR}#g" "$WIDGET_SCRIPT" 2>/dev/null || perl -pi -e "s#__REPO_DIR__#${REPO_DIR}#g" "$WIDGET_SCRIPT"
chmod +x "$WIDGET_SCRIPT"

echo "Created advanced Termux widget script: $WIDGET_SCRIPT"
echo "This widget will now automatically handle dependencies, personas, and server startup with a single tap."
