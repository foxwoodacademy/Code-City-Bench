#!/bin/bash
cd /storage/emulated/0/RootBase/citybridge
python3 bridge.py &
echo $! > .pid
sleep 1
curl -s http://127.0.0.1:8766 || echo "Bridge failed"
