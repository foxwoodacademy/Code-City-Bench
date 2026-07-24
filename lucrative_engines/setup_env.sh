#!/bin/bash
# Setup script for lucrative engines
ROOT="/storage/emulated/0/RootBase"

echo "Configuring environment..."

# Ensure directories exist
mkdir -p "$ROOT/lucrative_engines/web3_trading"

# Create .env from example if it doesn't exist
if [ -f "$ROOT/lucrative_engines/web3_trading/.env.example" ] && [ ! -f "$ROOT/lucrative_engines/web3_trading/.env" ]; then
    cp "$ROOT/lucrative_engines/web3_trading/.env.example" "$ROOT/lucrative_engines/web3_trading/.env"
    echo "Created .env from .env.example"
fi

echo "Environment configuration complete. Check MRD.txt for manual tasks."
