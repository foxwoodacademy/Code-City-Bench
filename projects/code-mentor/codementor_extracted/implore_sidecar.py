#!/usr/bin/env python3
"""
IMPLORE SIDECAR: Codebase Scanner for Grant Intelligence
"""
import os
import json
import argparse
from pathlib import Path

class ImploreScanner:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.profile = {
            "languages": {},
            "dependencies": [],
            "readme_content": "",
            "technical_signals": [],
            "impact_signals": []
        }

    def scan(self):
        """Walk the directory and generate a ProjectProfile"""
        for root, dirs, files in os.walk(self.root_dir):
            for file in files:
                filepath = Path(root) / file
                
                # Language count
                ext = filepath.suffix
                if ext:
                    self.profile["languages"][ext] = self.profile["languages"].get(ext, 0) + 1
                
                # README capture
                if file.lower() == "readme.md":
                    self.profile["readme_content"] = filepath.read_text(encoding='utf-8', errors='ignore')[:5000]

                # Dependency detection (simple approach)
                if file in ['package.json', 'requirements.txt', 'Cargo.toml']:
                    self.profile["dependencies"].append(str(filepath))

        return self.profile

def main():
    parser = argparse.ArgumentParser(description="Implore Sidecar: Codebase Scanner")
    parser.add_argument("directory", help="Directory to scan")
    args = parser.parse_args()
    
    scanner = ImploreScanner(args.directory)
    profile = scanner.scan()
    
    output_file = "project_profile.json"
    with open(output_file, "w") as f:
        json.dump(profile, f, indent=2)
    
    print(f"✅ Generated {output_file}")
    print(json.dumps(profile, indent=2)[:500] + "...")

if __name__ == "__main__":
    main()
