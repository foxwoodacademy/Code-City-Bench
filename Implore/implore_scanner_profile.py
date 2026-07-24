import json
from pathlib import Path

class ProfileBuilder:
    def __init__(self):
        self.profile = {
            "languages": {},
            "dependencies": [],
            "readme_content": "",
            "technical_signals": [],
            "impact_signals": []
        }

    def update_with_file(self, filepath):
        # Language count
        ext = filepath.suffix
        if ext:
            self.profile["languages"][ext] = self.profile["languages"].get(ext, 0) + 1
        
        # README capture
        if filepath.name.lower() == "readme.md":
            self.profile["readme_content"] = filepath.read_text(encoding='utf-8', errors='ignore')[:5000]

        # Dependency detection
        if filepath.name in ['package.json', 'requirements.txt', 'Cargo.toml']:
            self.profile["dependencies"].append(str(filepath))

    def get_profile(self):
        return self.profile
