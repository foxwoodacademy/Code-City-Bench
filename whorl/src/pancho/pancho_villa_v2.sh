#!/bin/bash

# PANCHO VILLA v2 -- Orchestrator with MEATWATCH constraint parsing
#
# Usage: ./pancho_villa.sh "your prompt here"
#
# Instead of firing all 9 agents regardless of what you ask for, Pancho now:
# 1. Parses your prompt with MEATWATCH to extract constraints
# 2. Determines which agents you actually need
# 3. Fires them in surgical order with proper handoff
# 4. Reports execution status as it goes

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEATWATCH="${SCRIPT_DIR}/meatwatch_v2.py"
WORK_DIR="${WORK_DIR:-.}"
LOG_DIR="${WORK_DIR}/.pancho-logs"

# Make sure meatwatch exists
if [ ! -f "$MEATWATCH" ]; then
    echo "✕ MEATWATCH not found at $MEATWATCH"
    exit 1
fi

mkdir -p "$LOG_DIR"

# --- Parse input ---
if [ -z "$1" ]; then
    echo "PANCHO VILLA v2"
    echo "==============="
    echo ""
    echo "Usage: ./pancho_villa.sh \"<your prompt>\""
    echo ""
    echo "Example:"
    echo "  ./pancho_villa.sh \"Build a Python backend that plays well with"
    echo "    React, deploy to Render, and document the API.\""
    echo ""
    echo "MEATWATCH will detect your constraints and fire the right agents."
    exit 1
fi

PROMPT="$1"

# --- Run MEATWATCH ---
echo "🔍 MEATWATCH analyzing constraints..."
PLAN=$(python3 "$MEATWATCH" "$PROMPT")
echo "$PLAN"
echo ""

# Extract the agents from MEATWATCH output (the "AGENTS TO INVOKE" section)
# This is a simplification; in production you'd parse JSON instead
AGENTS=$(echo "$PLAN" | grep -A 20 "AGENTS TO INVOKE" | grep "^  [0-9]" | awk '{print $3}' | tr '[:upper:]' '[:lower:]')

if [ -z "$AGENTS" ]; then
    echo "⚠ MEATWATCH detected no agents. Check your prompt."
    exit 1
fi

echo "Firing agents: $AGENTS"
echo ""

# --- Agent executors ---
# Each agent is mapped to the CLI tool that runs it
declare -A AGENT_CMD=(
    [gemini]="gemini cli"
    [freebuff]="freebuff"
    [vibe]="tsx /data/data/com.termux/files/usr/lib/node_modules/vibe-cli/index.ts"
    [pytch]="python3 Pytch/pytch.py --mode docs"
    [vertical-ai]="python3 /path/to/vertical_ai.py"
    [dna]="python3 scripts/dna.py"
    [molt]="python3 molt_watchdog.py"
    [front-desk]="python3 front_desk_lady.py"
    [zeroclaw]="python3 zeroclaw-android/bridge.py --deploy"
)

# --- Fire agents in order (with tmux, one window per agent) ---
run_agent() {
    local agent="$1"
    local prompt="$2"
    local log="${LOG_DIR}/${agent}.log"
    
    echo "🚀 Launching $agent..."
    
    # Get the base command for this agent
    local cmd="${AGENT_CMD[$agent]}"
    if [ -z "$cmd" ]; then
        echo "  ⚠ No command configured for $agent"
        return 1
    fi
    
    # Run in a tmux window (new window per agent, they run in parallel)
    # If tmux isn't available, run in background instead
    if command -v tmux &>/dev/null; then
        tmux new-window -n "$agent" "$cmd \"$prompt\"" 2>/dev/null || \
            (eval "$cmd \"$prompt\"" > "$log" 2>&1 &)
    else
        (eval "$cmd \"$prompt\"" > "$log" 2>&1 &)
    fi
    
    echo "  ✓ $agent running (log: $log)"
}

# Fire the agents that MEATWATCH identified
DEPLOY_TARGET=$(echo "$PLAN" | grep "DEPLOY TARGET" | awk '{print $NF}' 2>/dev/null)

for agent in $AGENTS; do
    # Customize the prompt per agent (each becomes a lead dev for their task)
    AGENT_PROMPT="You are the lead developer for the '$agent' phase. $PROMPT"
    
    # If this is the deploy agent and we detected a target, add that context
    if [ "$agent" = "zeroclaw" ] && [ -n "$DEPLOY_TARGET" ]; then
        AGENT_PROMPT="$AGENT_PROMPT Deploy to: $DEPLOY_TARGET"
    fi
    
    run_agent "$agent" "$AGENT_PROMPT"
    sleep 1  # stagger the starts slightly
done

echo ""
echo "✓ PANCHO VILLA workflow initiated"
echo "  Agents running in parallel (tmux windows or background)"
echo "  Check $LOG_DIR/ for individual logs"
echo "  Run: tmux list-windows (if using tmux)"
echo ""
