#!/usr/bin/env bash

clear
echo "=========================================="
echo "    TERMUX LOCAL RAM PLUS INJECTOR        "
echo "=========================================="

echo "[*] Starting local ADB server..."
adb start-server

echo "[!] Note: You must be on Wi-Fi or have a hotspot enabled for this to work."
echo "------------------------------------------"
echo "1. Go to Developer Options -> Wireless Debugging."
echo "2. Tap 'Pair device with pairing code'."
echo "------------------------------------------"

read -p "[?] Enter the IP & Port (e.g., 192.168.1.50:39455): " ip_port
read -p "[?] Enter the 6-digit Pairing Code: " pair_code

echo "[*] Attempting to pair locally..."
adb pair "$ip_port" "$pair_code"

echo -e "\n[*] Look at the Wireless Debugging main screen now."
read -p "[?] Enter the dynamic 'IP address & port' shown on the main screen: " connect_port

echo "[*] Connecting to local system..."
adb connect "$connect_port"

# Verify connection
DEVICE_CHECK=$(adb devices | grep -E "device$" | wc -l)
if [ "$DEVICE_CHECK" -eq 0 ]; then
    echo "[-] Connection failed. Please check ports and try again."
    exit 1
fi

echo "[+] Connected to self! Injecting RAM options..."
adb shell settings put global ram_expand_size_list 0,2,4,6,8,12,16

if [ $? -eq 0 ]; then
    echo "[SUCCESS] Memory table updated!"
    echo "[*] Rebooting your phone now to finalize..."
    sleep 2
    adb reboot
else
    echo "[-] Injection failed. Ensure permissions were granted."
fi
