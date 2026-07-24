#!/bin/bash

# Define clear, readable tracking variables
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/storage/emulated/0/RootBase/Backups/Snapshot_${TIMESTAMP}"
mkdir -p "$BACKUP_DIR"

echo "=================================================="
echo " LOUGH BIOMETRIC SYSTEM BACKUP UTILITY"
echo "=================================================="
echo "[*] Initializing archive target directory..."

# Copy all active development source files and assets
cp /storage/emulated/0/RootBase/telemetry_test.cpp "$BACKUP_DIR/"
cp /storage/emulated/0/RootBase/lough_daemon.py "$BACKUP_DIR/"
cp /storage/emulated/0/RootBase/read_logs.py "$BACKUP_DIR/"
cp $HOME/telemetry_bin "$BACKUP_DIR/"

# Safely verify if database file exists before copying
if [ -f "/storage/emulated/0/RootBase/lough_telemetry.db" ]; then
    cp /storage/emulated/0/RootBase/lough_telemetry.db "$BACKUP_DIR/"
    echo "[->] Telemetry SQLite Ledger backed up successfully."
else
    echo "[!] Notice: Active database ledger not found yet. Skipping database copy."
fi

echo "[->] C++ source code and verification binaries archived."
echo "=================================================="
echo " SUCCESS: System state secured at:"
echo " ${BACKUP_DIR}"
echo "=================================================="
