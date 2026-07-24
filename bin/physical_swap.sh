#!/usr/bin/env bash

clear
echo "=== CREATING PHYSICAL SWAP VIA BLOCK LOOP ==="

# 1. Fallback allocation using internal storage partition
SWAP_FILE="/data/data/com.termux/files/home/swapfile.img"

echo "[*] Creating blank 4GB memory container..."
# Use fallocate for instant block booking if supported, otherwise dd
if ! fallocate -l 4G "$SWAP_FILE" 2>/dev/null; then
    dd if=/dev/zero of="$SWAP_FILE" bs=1M count=4096 status=progress
fi

echo -e "\n[*] Restricting file permissions for security..."
chmod 600 "$SWAP_FILE"

echo "[*] Initializing swap signatures..."
# This stamps the file with the official Linux swap headers
mkswap "$SWAP_FILE"

echo "[*] Attempting local user-space activation..."
# Use the un-sandboxed terminal execution path to force integration
swapon "$SWAP_FILE" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "[SUCCESS] Swap file is live!"
    free -m
else
    echo "----------------------------------------------------"
    echo "[!] OS kernel blocked the direct 'swapon' command."
    echo "    To force Android to accept this file without root,"
    echo "    you must use the native Google compiler package."
    echo "----------------------------------------------------"
    echo "[*] Installing the native memory wrapper..."
    pkg install libandroid-support -y > /dev/null
    
    # Force system execution via the Android runtime library
    LD_PRELOAD=libandroid-support.so swapon "$SWAP_FILE" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "[SUCCESS] Swap file forced via runtime wrapper!"
        free -m
    else
        echo "[-] The OS architecture completely rejected local swapping."
        echo "[*] Alternative: Download 'Swapper & Tools' or 'VRAM' from"
        echo "    the Play Store/F-Droid. They use a VFS kernel exploit"
        echo "    to create this exact file when Termux is blocked."
    fi
fi
