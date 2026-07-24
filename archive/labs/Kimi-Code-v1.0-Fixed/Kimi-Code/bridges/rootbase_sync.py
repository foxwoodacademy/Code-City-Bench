"""
Kimi-Code ↔ RootBase Sync
Synchronizes with the broader RootBase ecosystem.
"""
import json
import os
import shutil
from datetime import datetime
from typing import Dict, List

class RootBaseSync:
    """Syncs Kimi-Code with RootBase ecosystem."""

    def __init__(self, state_engine, rootbase_path: str = None):
        self.state = state_engine
        self.rootbase = rootbase_path or "/storage/emulated/0/RootBase"
        self.kimi_dir = os.path.join(self.rootbase, "Kimi-Code")

    def sync_all(self):
        """Full sync operation."""
        self._ensure_directory_structure()
        self._sync_state()
        self._sync_analytics()
        self._sync_reports()
        self._create_manifest()

    def _ensure_directory_structure(self):
        """Create Kimi-Code directory in RootBase."""
        dirs = ["data", "reports", "exports", "backups"]
        for d in dirs:
            os.makedirs(os.path.join(self.kimi_dir, d), exist_ok=True)

    def _sync_state(self):
        """Sync user state to RootBase."""
        state_export = os.path.join(self.kimi_dir, "data", "user_state.json")

        # Create sanitized export (no API keys)
        safe_state = {
            "user_id": self.state.state.get("user_id"),
            "global_level": self.state.state.get("global_level"),
            "global_xp": self.state.state.get("global_xp"),
            "skill_tree": self.state.state.get("skill_tree"),
            "hats_mastery": self.state.state.get("hats_mastery"),
            "languages": {
                lang: {
                    "level": data["level"],
                    "mastery_score": data["mastery_score"]
                }
                for lang, data in self.state.state.get("languages", {}).items()
            },
            "achievements": self.state.state.get("achievements", []),
            "streak_days": self.state.state.get("streak_days"),
            "total_challenges": self.state.state.get("total_challenges_completed"),
            "last_sync": datetime.now().isoformat()
        }

        with open(state_export, 'w') as f:
            json.dump(safe_state, f, indent=2)

    def _sync_analytics(self):
        """Sync analytics data."""
        source = os.path.join(os.path.dirname(__file__), '..', 'data', 'challenge_history.jsonl')
        dest = os.path.join(self.kimi_dir, "data", "challenge_history.jsonl")

        if os.path.exists(source):
            shutil.copy2(source, dest)

    def _sync_reports(self):
        """Sync generated reports."""
        reports_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        dest_dir = os.path.join(self.kimi_dir, "reports")

        for f in os.listdir(reports_dir):
            if f.startswith('report_') and f.endswith('.html'):
                shutil.copy2(os.path.join(reports_dir, f), dest_dir)

    def _create_manifest(self):
        """Create sync manifest."""
        manifest = {
            "project": "Kimi-Code",
            "version": "1.0.0",
            "last_sync": datetime.now().isoformat(),
            "synced_items": {
                "user_state": True,
                "analytics": True,
                "reports": True,
                "codementor_bridge": os.path.exists(os.path.join(self.rootbase, "CodeMentor-MVP"))
            },
            "paths": {
                "state": "data/user_state.json",
                "analytics": "data/challenge_history.jsonl",
                "reports": "reports/"
            }
        }

        with open(os.path.join(self.kimi_dir, "manifest.json"), 'w') as f:
            json.dump(manifest, f, indent=2)

    def import_from_rootbase(self):
        """Import data from other RootBase projects."""
        # Import from CodeMentor
        cm_bridge_path = os.path.join(self.rootbase, "CodeMentor-MVP")
        if os.path.exists(cm_bridge_path):
            from .codementor_bridge import CodeMentorBridge
            bridge = CodeMentorBridge(self.state, cm_bridge_path)
            bridge.sync_analytics()

        # Could extend to other projects (Thoth, Hermes, etc.)
        return {"imported": True}
