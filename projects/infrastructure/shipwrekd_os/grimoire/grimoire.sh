#!/bin/bash
# GRIMOIRE — ShipWrekD OS Shell Layer
# Source this in .bashrc: source /storage/emulated/0/RootBase/shipwrekd_os/grimoire/grimoire.sh

export SHIPWREKD_ROOT="/storage/emulated/0/RootBase"
export SYNTAX_LOG_DIR="$SHIPWREKD_ROOT/whorl/syntax_sessions"
export PATH="$PATH:$SHIPWREKD_ROOT/bin"

# Syntax alias
alias syntax="python3 $SHIPWREKD_ROOT/syntax.py"
alias syn="syntax"

# Quick nav
alias rb="cd $SHIPWREKD_ROOT"
alias whorl="cd $SHIPWREKD_ROOT/whorl"
alias lough="cd $SHIPWREKD_ROOT/lough_system"

# Tree
alias tree-rb="bash $SHIPWREKD_ROOT/tree_scan.sh"

echo "[GRIMOIRE] ShipWrekD OS loaded. Syntax standing by."
