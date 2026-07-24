#!/usr/bin/env bash
# Lead developer convenience script: sets aliases, starts scheduler (preview-only) and prints next steps
set -euo pipefail
ROOT=${1:-/storage/emulated/0/RootBase}
RC=${2:-~/.bashrc}
ALIAS="alias bardildo='python3 $ROOT/tools/bardildo/bardildo.py --root $ROOT --write --headless'"

echo "# Bardildo alias (add to your shell rc):" > /tmp/bardildo_alias.txt
echo "$ALIAS" >> /tmp/bardildo_alias.txt
echo "Alias snippet written to /tmp/bardildo_alias.txt. Append to your shell rc: $RC"

# Start scheduled scanner in background (preview-only summary)
export BARD_ROOT="$ROOT"
export TMPDIR=${TMPDIR:-/data/data/com.termux/files/usr/tmp}
nohup python3 "$ROOT/tools/bardildo/scheduled_scan.py" > "$TMPDIR/bardildo_schedule.log" 2>&1 &
echo $! > "$TMPDIR/bardildo_schedule.pid"

cat <<EOF
Started scheduled scan (preview-only). PID: $(cat $TMPDIR/bardildo_schedule.pid)
Log: $TMPDIR/bardildo_schedule.log
Next steps:
 - Edit persona_map.json to map Modelfile names to personas.
 - If Ollama is available, set OLLAMA_URI and test ollama-backed buddies.
 - Use the TUI: python3 $ROOT/tools/bardildo/tui.py
EOF
