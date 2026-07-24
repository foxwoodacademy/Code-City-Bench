#!/bin/bash

# Sovereign Swarm Tmux Session Manager
# Launches a pre-configured tmux session for comprehensive swarm oversight.

SESSION_NAME="SovereignSwarm"

# --- Check if tmux is installed ---
if ! command -v tmux &> /dev/null
then
    echo "[ERROR] tmux is not installed. Please install it first: pkg install tmux"
    exit 1
fi

# --- Check if session already exists ---
if tmux has-session -t $SESSION_NAME 2>/dev/null;
then
    echo "Session '$SESSION_NAME' already exists. Attaching..."
    tmux attach-session -t $SESSION_NAME
    exit 0
fi

# --- Create new tmux session ---
echo "[SYS] Creating new tmux session: $SESSION_NAME"

# Create the session and the first window
tmux new-session -d -s $SESSION_NAME -n "THOTH_UI"

# Set window 0 (Thoth UI)
# Run Thoth UI in the first pane
tmux send-keys -t $SESSION_NAME:0.0 "python3 /storage/emulated/0/RootBase/thoth_orchestrator/thoth_ui.py"

# Create Window 1: Monitoring
tmux new-window -t $SESSION_NAME:1 -n "MONITOR"
sleep 1 # Give it a moment
tmux split-window -v -p 50 # Split vertically
tmux select-pane -t 0
tmux send-keys "tail -f /storage/emulated/0/RootBase/lough_system/lough.log" C-m
tmux select-pane -t 1
tmux send-keys "tail -f /storage/emulated/0/RootBase/web_server/websocket.log" C-m
tmux split-window -h -p 50 # Split the active pane horizontally
tmux select-pane -t 0 # Go back to the top-left pane
tmux send-keys "tail -f /storage/emulated/0/RootBase/nursery/molt.log || tail -f /storage/emulated/0/RootBase/swarm_motion.log" C-m

# Create Window 2: Thoth CLI
tmux new-window -t $SESSION_NAME:2 -n "THOTH_CLI"
sleep 1
tmux send-keys "python3 /storage/emulated/0/RootBase/thoth_orchestrator/thoth.py --watch" C-m

# Create Window 3: Vibe/Codex Interactive Shells
tmux new-window -t $SESSION_NAME:3 -n "AGENT_SHELLS"
sleep 1
tmux split-window -h -p 50
tmux select-pane -t 0
tmux send-keys "echo "Starting Vibe CLI..."; exec python3 /storage/emulated/0/RootBase/mrs_higgins_saas/firefly_scout.py --watch" C-m
tmux select-pane -t 1
tmux send-keys "echo "Starting Codex CLI..."; # Assuming codex has a CLI, or you will specify one. Adjust if needed. exec python3 /storage/emulated/0/RootBase/codex_install/codex_cli.py" C-m # Placeholder for Codex CLI

# Create Window 4: System Monitoring
tmux new-window -t $SESSION_NAME:4 -n "SYSTEM_MONITOR"
sleep 1
tmux send-keys "htop"

# Attach to the session
echo "[SYS] Attaching to '$SESSION_NAME' session..."
tmux attach-session -t $SESSION_NAME
