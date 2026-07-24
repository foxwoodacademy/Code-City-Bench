#!/bin/bash

# Sovereign Swarm Startup Script
# This script initializes the entire agentic ecosystem.

# --- Environment Setup ---
export PATH=$PATH:/storage/emulated/0/RootBase/bin
export PATH=$PATH:/storage/emulated/0/RootBase/codex_install/node_modules/.bin

# Source Zoxide for navigation assistance
if [ -f /data/data/com.termux/files/home/.bashrc ]; then
    source /data/data/com.termux/files/home/.bashrc
fi

# --- Initialization Sequence ---
echo "[SYS] Bootstrapping Sovereign Swarm..."

# 1. Start the Lough Event Spine (Real-time Audit)
if ! pgrep -f "field_server.py" > /dev/null; then
    echo "[LOUGH] Initializing Lough Event Spine..."
    nohup python3 /storage/emulated/0/RootBase/lough_system/lough_system/field_server.py > /storage/emulated/0/RootBase/lough_system/lough.log 2>&1 &
    sleep 2 # Give it a moment to bind
else
    echo "[LOUGH] Event Spine already running."
fi

# 2. Start the Websocket Server (Dashboard Heartbeat)
if ! pgrep -f "ws_server.py" > /dev/null; then
    echo "[WEB] Initializing Websocket Heartbeat..."
    nohup python3 /storage/emulated/0/RootBase/web_server/Websocket/ws_server.py > /storage/emulated/0/RootBase/web_server/websocket.log 2>&1 &
    sleep 2 # Give it a moment to bind
else
    echo "[WEB] Websocket Heartbeat already running."
fi

# 3. Activate Thoth Command Center & UI
if ! pgrep -f "thoth_ui.py" > /dev/null; then
    echo "[THOTH] Booting Command Center..."
    # Run Thoth UI in the foreground for interaction
    python3 /storage/emulated/0/RootBase/thoth_orchestrator/thoth_ui.py
else
    echo "[THOTH] Command Center already running."
fi

# 4. Trigger Initial Firefly Scout Scan (Optional - if not running Thoth UI)
# The Thoth UI can trigger this, but for a full startup, we can ensure it runs.
# if ! pgrep -f "thoth.py" > /dev/null; then
#     echo "[FIREFLY] Initiating initial market scan..."
#     python3 /storage/emulated/0/RootBase/thoth_orchestrator/thoth.py --scout-and-analyze &
# fi

echo "[SYS] Sovereign Swarm initialized and running."
