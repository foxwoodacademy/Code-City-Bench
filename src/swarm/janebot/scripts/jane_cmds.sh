#!/bin/bash

# JaneBot Orchestration Aliases
# Add this to ~/.bashrc: source ~/janebot-motherbrain/scripts/jane_cmds.sh

PROJECT_ROOT="$HOME/janebot-motherbrain"
UI_DIR="$PROJECT_ROOT/swarm_ui"
PORT=8080

function jane() {
    case "$1" in
        boot)
            echo "🚀 Booting MotherBrain UI..."
            cd "$UI_DIR" || return
            # Start HTTP server in background
            python3 -m http.server $PORT > /dev/null 2>&1 &
            SERVER_PID=$!
            echo $SERVER_PID > "$PROJECT_ROOT/.server_pid"
            
            # Wake lock for persistence
            termux-wake-lock
            
            # Open UI in Chrome
            termux-open-url "http://localhost:$PORT/index.html"
            echo "✅ UI launched at http://localhost:$PORT"
            ;;
        status)
            echo "📊 Checking Swarm Status..."
            if [ -f "$PROJECT_ROOT/.server_pid" ]; then
                PID=$(cat "$PROJECT_ROOT/.server_pid")
                if ps -p "$PID" > /dev/null; then
                    echo "✅ UI Server: RUNNING (PID: $PID)"
                else
                    echo "❌ UI Server: STOPPED"
                fi
            else
                echo "❌ UI Server: NOT STARTED"
            fi
            
            # Check for Python MotherBrain process
            if pgrep -f "janebot_motherbrain" > /dev/null; then
                echo "✅ MotherBrain Core: RUNNING"
            else
                echo "❌ MotherBrain Core: NOT RUNNING"
            fi
            ;;
        stop)
            echo "🛑 Stopping MotherBrain..."
            if [ -f "$PROJECT_ROOT/.server_pid" ]; then
                PID=$(cat "$PROJECT_ROOT/.server_pid")
                kill "$PID" 2>/dev/null
                rm "$PROJECT_ROOT/.server_pid"
                echo "✅ UI Server stopped."
            fi
            pkill -f "janebot_motherbrain"
            termux-wake-unlock
            echo "✅ All processes stopped."
            ;;
        init)
            echo "🛠️ Initializing Swarm Environment..."
            pip install -r "$PROJECT_ROOT/requirements.txt"
            echo "✅ Environment ready."
            ;;
        *)
            echo "Usage: jane {boot|status|stop|init}"
            ;;
    esac
}
