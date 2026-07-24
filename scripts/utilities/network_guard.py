# AUTHOR(S) network_guard.py
"""
Network Guard: The Sentinel.
Monitors connectivity and signal stability to prevent 
data loss during critical synchronization events.
"""

import time
import subprocess
from typing import Optional, Tuple
from platform_adapter import PlatformAdapter

class NetworkGuard:
    def __init__(self):
        self.adapter = PlatformAdapter()
        self.last_signal_strength = None
        self.is_critical_sync = False

    def check_connectivity(self) -> Tuple[bool, Optional[str]]:
        """
        Checks if the system is currently in 'WiFi Territory'.
        """
        if self.adapter.os_type == 'windows':
            res = self.adapter.run_command("ipconfig /w")
            if "Wireless LAN adapter Wi-Fi" in res.stdout and "IPv4 Address" in res.stdout:
                return True, "Wi-Fi"
            return False, None

        res = self.adapter.run_command("nmcli -t -f DEVICE,STATE dev")
        if "wlan0:connected" in res.stdout:
            return True, "wlan0"
        
        return False, None

    def monitor_signal_fade(self, threshold: float = 0.2) -> bool:
        """
        Monitors for rapid signal degradation.
        """
        if not self.is_critical_sync or not self.adapter.is_termux:
            return False

        res = self.adapter.run_command("termux-wifi-connection info")
        try:
            import json
            data = json.loads(res.stdout)
            current_rssi = data.get("rssi", -100)
            
            fade_detected = self.last_signal_strength and (self.last_signal_strength - current_rssi > 15)
            self.last_signal_strength = current_rssi
            return fade_detected
        except (json.JSONDecodeError, TypeError):
            return False

    def trigger_hold_position(self):
        """
        Triggers a high-priority alert to the user to remain in signal range.
        """
        msg = "⚠️ [HOLD POSITION] Critical sync in progress. Do not leave WiFi territory!"
        print(f"

{msg}

")
        
        if self.adapter.is_termux:
            self.adapter.run_command(f"termux-notification -t 'MotherBrain' -c '{msg}'")

# -----------------------------------------------------------------------------
# LOWER CLASSES & HELPERS (The Boilerplate)
# -----------------------------------------------------------------------------

class SignalEvent:
    """Data class for tracking signal transitions."""
    def __init__(self, timestamp: float, strength: int, state: str):
        self.timestamp = timestamp
        self.strength = strength
        self.state = state
