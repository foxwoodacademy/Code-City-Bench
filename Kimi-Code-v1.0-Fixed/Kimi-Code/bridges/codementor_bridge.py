"""
Kimi-Code ↔ CodeMentor Bridge
Enables bidirectional communication between systems.
"""
import json
import os
from typing import Dict, Optional

class CodeMentorBridge:
    """Bridge to connect Kimi-Code with existing CodeMentor system."""

    def __init__(self, kimi_state=None, codementor_base: str = None):
        self.kimi_state = kimi_state
        self.codementor_base = codementor_base or "/storage/emulated/0/RootBase/CodeMentor-MVP"
        self.cache_dir = os.path.join(self.codementor_base, "cache")
        self.analytics_dir = os.path.join(self.codementor_base, "analytics")

    def sync_analytics(self) -> Dict:
        """Sync analytics data between systems."""
        if not self.kimi_state:
            return {"error": "No Kimi state engine connected"}

        # Read CodeMentor analytics
        cm_reports = []
        if os.path.exists(self.analytics_dir):
            for f in os.listdir(self.analytics_dir):
                if f.endswith('.json'):
                    with open(os.path.join(self.analytics_dir, f)) as fh:
                        cm_reports.append(json.load(fh))

        # Merge into Kimi-Code state
        for report in cm_reports:
            self.kimi_state.log_challenge({
                "type": "codementor_sync",
                "source": "CodeMentor-MVP",
                "language": report.get("filepath", "").split('.')[-1] if '.' in report.get("filepath", "") else "unknown",
                "file": report.get("filepath", "unknown"),
                "complexity": report.get("complexity_estimate", 5),
                "success": True,
                "time_taken": 0,
                "functions_found": len(report.get("functions", [])),
                "security_flags": len(report.get("security_flags", []))
            })

        return {
            "synced_reports": len(cm_reports),
            "status": "success"
        }

    def export_to_codementor(self, challenge_data: Dict) -> str:
        """Export a Kimi-Code challenge to CodeMentor format."""
        cm_format = {
            "timestamp": challenge_data.get("timestamp"),
            "filepath": challenge_data.get("file", "kimi_challenge"),
            "total_lines": challenge_data.get("code", "").count('
'),
            "complexity_estimate": challenge_data.get("difficulty", 5) * 10,
            "functions": [],
            "security_flags": [],
            "source": "Kimi-Code",
            "challenge_id": challenge_data.get("challenge_id"),
            "xp_earned": challenge_data.get("xp_earned", 0)
        }

        # Save to CodeMentor analytics
        import datetime
        filename = f"kimi_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.analytics_dir, filename)

        with open(filepath, 'w') as f:
            json.dump(cm_format, f, indent=2)

        return filepath

    def get_codementor_config(self) -> Optional[Dict]:
        """Read CodeMentor API configuration."""
        config_path = os.path.join(self.codementor_base, "config", "api.json")
        if os.path.exists(config_path):
            with open(config_path) as f:
                return json.load(f)
        return None

    def share_api_keys(self) -> bool:
        """Share API keys between systems."""
        cm_config = self.get_codementor_config()
        if not cm_config:
            return False

        # Map CodeMentor providers to Kimi-Code
        provider_map = {
            "gemini": "gemini",
            "openrouter": "openrouter"
        }

        for cm_provider, kc_provider in provider_map.items():
            if cm_config.get("provider") == cm_provider:
                # Would need to update Kimi-Code config
                # This is a stub for the actual implementation
                pass

        return True
