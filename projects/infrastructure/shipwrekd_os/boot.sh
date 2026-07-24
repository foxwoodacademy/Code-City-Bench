#!/bin/bash
# SHIPWREKD OS — BOOT SEQUENCE
# Run this once after fresh Termux install or device reset

ROOT="/storage/emulated/0/RootBase"

echo "╔══════════════════════════════════════╗"
echo "║      SHIPWREKD OS — BOOTING          ║"
echo "╚══════════════════════════════════════╝"

# Load GRIMOIRE
source "$ROOT/shipwrekd_os/grimoire/grimoire.sh"

# Start Molt supervisor if present
[ -f "$ROOT/molt_bleak/molt.py" ] && python3 "$ROOT/molt_bleak/molt.py" --daemon &

# Confirm Lough is writable
mkdir -p "$ROOT/lough_system/lough.log"

echo "[ShipWrekD] Systems nominal. Syntax standing by."
echo "[ShipWrekD] Type 'syntax' to wake the warden."
