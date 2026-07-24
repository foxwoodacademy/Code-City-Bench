#!/usr/bin/env bash
# Create a Termux widget script that toggles the Vertical AI boardroom server.
# Usage: bash create_termux_widget.sh /path/to/RootBase/vertical_local

REPO_DIR="${1:-/storage/emulated/0/RootBase/vertical_local}"
SHORTCUT_DIR="$HOME/.shortcuts"
WIDGET_SCRIPT="$SHORTCUT_DIR/vertical_boardroom_widget.sh"

mkdir -p "$SHORTCUT_DIR"

cat > "$WIDGET_SCRIPT" <<'SH'
#!/usr/bin/env bash
# Toggle start/stop for Vertical AI boardroom
REPO_DIR="__REPO_DIR__"
SCRIPT="$REPO_DIR/run_boardroom.sh"
PIDFILE="${TMPDIR:-/data/data/com.termux/files/usr/tmp}/vertical_uvicorn.pid"

if [ -f "$PIDFILE" ]; then
  PID=$(cat "$PIDFILE" 2>/dev/null || true)
  if [ -n "$PID" ] && ps -p "$PID" > /dev/null 2>&1; then
    echo "Stopping server (pid $PID)" > /dev/null
    bash "$SCRIPT" stop
    exit 0
  fi
fi
# Start
bash "$SCRIPT" start
exit 0
SH

# Replace placeholder with actual path
sed -i "s#__REPO_DIR__#${REPO_DIR}#g" "$WIDGET_SCRIPT" 2>/dev/null || perl -pi -e "s#__REPO_DIR__#${REPO_DIR}#g" "$WIDGET_SCRIPT"
chmod +x "$WIDGET_SCRIPT"

echo "Created Termux widget script: $WIDGET_SCRIPT"
echo "Add Termux:Widget to your home screen and select 'vertical_boardroom_widget' to get a one-tap start/stop."
