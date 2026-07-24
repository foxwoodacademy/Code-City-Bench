#!/bin/bash
cd "$(dirname "$0")"
python3 bridge.py &
BRIDGE_PID=$!
echo "Bridge PID: $BRIDGE_PID"
echo "$BRIDGE_PID" > .bridge.pid
echo "Test with: curl http://127.0.0.1:8766/health"
