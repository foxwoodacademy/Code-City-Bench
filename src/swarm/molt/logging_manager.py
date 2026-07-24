import os
import json
import shutil
import ast
import time
from pathlib import Path
from typing import Dict, Any, Optional

class LoggingManager:
    def __init__(self, log_dir: str = "molt_v5_log"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.patch_log = self.log_dir / "patches.jsonl"
        self.audit_log = self.log_dir / "audit.log"

    def create_backup(self, file_path: Path):
        """Create a .bak snapshot of the file before modification."""
        if file_path.exists():
            backup_path = file_path.with_suffix(file_path.suffix + ".bak")
            shutil.copy2(file_path, backup_path)
            return backup_path
        return None

    def log_patch(self, file_path: str, action: str, lines: list, content: str):
        """Log a structured patch for Gemini CLI review."""
        patch = {
            "timestamp": time.time(),
            "file": file_path,
            "action": action,
            "lines": lines,
            "content": content
        }
        with open(self.patch_log, "a") as f:
            f.write(json.dumps(patch) + "\n")
        return patch

    @staticmethod
    def validate_syntax(code: str) -> bool:
        """Use AST to ensure code is valid before saving."""
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False

class SecurityAudit:
    @staticmethod
    def check_for_injection(prompt: str) -> bool:
        """Simple pattern check for common injection attempts."""
        forbidden = ["import os", "rm -rf", "eval(", "exec("]
        return any(f in prompt for f in forbidden)

# --- Example Usage Logic ---
# manager = LoggingManager()
# backup = manager.create_backup(Path("target.py"))
# if manager.validate_syntax(new_code):
#     manager.log_patch("target.py", "replace", [12, 24], new_code)
