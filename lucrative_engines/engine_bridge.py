import os
import json
import requests
from typing import Optional, Dict, Any

class EngineBridge:
    """
    Bridge between Lucrative Engines and Motherbrain ecosystem.
    Allows engines to report telemetry, status, and alerts.
    """
    
    def __init__(self, engine_name: str):
        self.engine_name = engine_name
        self.root = "/storage/emulated/0/RootBase"
        self.telemetry_path = os.path.join(self.root, "GRAB/telemetry")
        os.makedirs(self.telemetry_path, exist_ok=True)

    def report_status(self, status: str, metadata: Optional[Dict[str, Any]] = None):
        payload = {
            "engine": self.engine_name,
            "status": status,
            "metadata": metadata or {},
            "timestamp": requests.utils.quote(str(os.popen('date').read().strip()))
        }
        status_file = os.path.join(self.telemetry_path, f"{self.engine_name}_status.json")
        with open(status_file, "w") as f:
            json.dump(payload, f, indent=2)
        print(f"[EngineBridge] {self.engine_name} status reported: {status}")

    def log_alert(self, level: str, message: str):
        alert = f"[{level.upper()}] {self.engine_name}: {message}\n"
        alert_file = os.path.join(self.root, "lucrative_engines/alerts.log")
        with open(alert_file, "a") as f:
            f.write(alert)

if __name__ == "__main__":
    bridge = EngineBridge("test_engine")
    bridge.report_status("active", {"test": True})
