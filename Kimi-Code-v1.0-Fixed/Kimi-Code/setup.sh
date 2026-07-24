#!/bin/bash
# Kimi-Code Setup Script for Termux/RootBase
set -e

BASE="/storage/emulated/0/RootBase/Kimi-Code"
REPO="$PWD"

echo "🧠 Kimi-Code Setup"
echo "=================="

# Create RootBase symlink/link
if [ ! -d "$BASE" ]; then
    mkdir -p "$BASE"
    echo "[+] Created $BASE"
fi

# Copy project files
cp -r "$REPO"/* "$BASE/"
echo "[+] Copied files to RootBase"

# Make scripts executable
chmod +x "$BASE/kimi_code.py"
chmod +x "$BASE/setup.sh"
chmod +x "$BASE/bin/"* 2>/dev/null || true

# Create symlink for easy access
if [ ! -f "$PREFIX/bin/kimi-code" ]; then
    ln -s "$BASE/kimi_code.py" "$PREFIX/bin/kimi-code"
    echo "[+] Created kimi-code command"
fi

# Initialize data directory
mkdir -p "$BASE/data"
mkdir -p "$BASE/data/cache"
mkdir -p "$BASE/data/analytics"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  kimi-code --setup     # Configure API keys"
echo "  kimi-code --status    # Check your progress"
echo "  kimi-code --help      # See all commands"
echo ""
echo "Dashboard:"
echo "  kimi-code --dashboard # Start web UI on :8767"
echo ""
echo "For Six Thinking Hats mode:"
echo "  kimi-code --hats-mode python"
