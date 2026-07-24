#!/bin/bash
# Mrs. Higgins Cron Scheduler
# Runs shipping pipeline on schedule

ROOTBASE="/storage/emulated/0/RootBase"
LOGDIR="$ROOTBASE/mrs_higgins_saas/logs"
mkdir -p "$LOGDIR"

TIMESTAMP=$(date '+%Y-%m-%d_%H:%M:%S')
LOGFILE="$LOGDIR/higgins_run_$TIMESTAMP.log"

export LIGHTNING_ADDRESS="ironicjewel052@walletofsatoshi.com"

cd "$ROOTBASE/mrs_higgins_saas"
python3 front_desk_lady.py >> "$LOGFILE" 2>&1

if [ $? -eq 0 ]; then
    echo "[✓] Mrs. Higgins run completed: $TIMESTAMP" >> "$LOGFILE"
else
    echo "[✗] Mrs. Higgins run failed: $TIMESTAMP" >> "$LOGFILE"
fi
