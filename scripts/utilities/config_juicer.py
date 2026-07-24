#!/usr/bin/env python3
# SOURCE: /storage/emulated/0/RootBase/scripts/utilities/config_juicer.py
# AUTHOR: foxwoodacademy
# PURPOSE: Universal configuration loader for AI model selection and API key management

import os
import sys
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml")
    sys.exit(1)

ROOTBASE = Path("/storage/emulated/0/RootBase")
CONFIG_FILE = ROOTBASE / "config_juicer.yaml"

class ConfigJuicer:
    def __init__(self, config_path=CONFIG_FILE):
        self.config_path = config_path
        self.config = {}
        self.keys = {}
        self._load_config()
        self.keys = self._load_keys()
    
    def _load_config(self):
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)
    
    def _load_keys(self):
        from dotenv import load_dotenv
        env_file = ROOTBASE / ".env"
        if env_file.exists():
            load_dotenv(env_file)
        
        keys = {}
        for provider in self.config.get("providers", {}).keys():
            key_var = f"{provider.upper()}_API_KEY"
            keys[provider] = os.getenv(key_var, "")
        return keys
    
    def get_tool_config(self, tool_name):
        if tool_name not in self.config.get("tools", {}):
            raise ValueError(f"Tool not found: {tool_name}")
        
        tool_cfg = self.config["tools"][tool_name].copy()
        primary = tool_cfg.get("primary_model")
        
        if primary:
            tool_cfg["api_key"] = self.keys.get(primary, "")
        
        return tool_cfg
    
    def validate(self):
        missing = [p for p, k in self.keys.items() if not k]
        if missing:
            print(f"Missing: {', '.join(missing)}")
            return False
        print("All keys validated")
        return True
    
    def print_status(self):
        print("\n" + "="*70)
        print("CONFIG JUICER STATUS")
        print("="*70 + "\n")
        
        print("VAULT:")
        for provider, key in sorted(self.keys.items()):
            status = "OK" if key else "MISSING"
            print(f"  {provider:15} [{status}]")
        
        print("\nTOOLS:")
        for tool, cfg in sorted(self.config.get("tools", {}).items()):
            model = cfg.get("primary_model", "N/A")
            print(f"  {tool:15} {model}")
        
        print("\n" + "="*70 + "\n")

def main():
    try:
        juicer = ConfigJuicer()
        
        if len(sys.argv) < 2:
            juicer.print_status()
            return 0
        
        cmd = sys.argv[1]
        
        if cmd == "status":
            juicer.print_status()
        elif cmd == "validate":
            return 0 if juicer.validate() else 1
        else:
            print("Commands: status, validate")
            return 1
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
