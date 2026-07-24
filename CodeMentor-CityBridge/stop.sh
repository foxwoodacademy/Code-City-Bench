#!/bin/bash
cd "$(dirname "$0")"
if [[ -f .bridge.pid ]]; then
    kill "$(cat .bridge.pid)" 2>/dev/null && echo "Bridge stopped" || echo "Already dead"
    rm .bridge.pid
else
    echo "No PID file found"
fi
