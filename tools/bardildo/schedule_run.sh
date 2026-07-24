#!/usr/bin/env bash
# Start scheduled scan in background (Termux-safe)
set -euo pipefail
ROOT=${1:-/storage/emulated/0/RootBase}
export BARD_ROOT="$ROOT"
export TMPDIR=${TMPDIR:-/data/data/com.termux/files/usr/tmp}
nohup python3 "$ROOT/tools/bardildo/scheduled_scan.py" > "$TMPDIR/bardildo_schedule.log" 2>&1 &
echo $! > "$TMPDIR/bardildo_schedule.pid"
echo "Scheduled scan started, pid=$(cat $TMPDIR/bardildo_schedule.pid), log=$TMPDIR/bardildo_schedule.log"
