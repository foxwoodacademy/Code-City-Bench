#!/usr/bin/env bash

clear
echo "=========================================="
echo "    TERMUX SAMSUNG CACHE & RAM PURGE      "
echo "=========================================="
echo "[*] Identifying memory-hogging background apps..."

# List of common Samsung and Android background resource hogs to terminate
TARGETS=(
    "com.facebook.services"
    "com.facebook.system"
    "com.facebook.appmanager"
    "com.google.android.gms.persistent"
    "com.samsung.android.smartswitchassistant"
    "com.samsung.android.bixby.agent"
    "com.samsung.android.kidshome"
    "com.sec.android.app.sbrowser"
    "com.microsoft.skydrive"
)

echo "[*] Killing background bloatware to free memory..."

# Loop through and forcefully kill background processing states
for app in "${TARGETS[@]}"; do
    # Using 'am kill' drops background states safely without crashing active UI
    am kill --user current "$app" > /dev/null 2>&1
    echo "[+] Evicted: $app"
done

echo "------------------------------------------"
echo "[*] Triggering internal Android memory garbage collection..."
# Force Dalvik/ART virtual machine cache compaction to squeeze free RAM out
cmd activity force-idle-maintenance > /dev/null 2>&1

echo "[SUCCESS] Background RAM cleared!"
echo "Check your Device Care settings to see your newly freed space."
