#!/usr/bin/env bash

echo "=========================================="
echo " ☣️  Installing CodeSmellSniffer Engine... "
echo "=========================================="

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    echo "[-] Error: Python3 is required but was not found on this system."
    exit 1
fi

# Make the sniffer executable
chmod +x sniffer.py

# Determine install location based on environment privileges
if [ -d "$PREFIX/bin" ]; then
    # Termux / Android environment
    INSTALL_DIR="$PREFIX/bin"
elif [ -d "/usr/local/bin" ]; then
    # Standard Linux / macOS environment
    INSTALL_DIR="/usr/local/bin"
else
    INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"
fi

echo "[+] Registering CLI binary to $INSTALL_DIR/smell-sniffer"

# Copy the file to the system path and rename it to a clean CLI command
cp sniffer.py "$INSTALL_DIR/smell-sniffer"
chmod +x "$INSTALL_DIR/smell-sniffer"

echo "=========================================="
echo "✅ Installation Complete!"
echo "You can now run the tool system-wide using:"
echo "   smell-sniffer <path_to_file>"
echo "=========================================="
