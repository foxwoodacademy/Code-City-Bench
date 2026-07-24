#!/usr/bin/env python3
# SOURCE: /storage/emulated/0/RootBase/scripts/integrations/env_generator.py
# AUTHOR: foxwoodacademy
# PURPOSE: Generate .env file from harvested keys. Auto-updates when new keys added.

import json
from pathlib import Path

ROOTBASE = Path("/storage/emulated/0/RootBase")
VAULT_FILE = ROOTBASE / "vault" / "keys" / "harvested_keys.json"
ENV_FILE = ROOTBASE / ".env"

def generate_env():
    """Generate .env from vault."""
    if not VAULT_FILE.exists():
        print("ERROR: No harvested keys found")
        return False
    
    with open(VAULT_FILE, 'r') as f:
        vault = json.load(f)
    
    env_lines = []
    env_lines.append("# AUTO-GENERATED from key_harvester")
    env_lines.append("# DO NOT EDIT MANUALLY - use key_harvester to add keys\n")
    
    for provider, info in sorted(vault.items()):
        if info.get("api_key"):
            key_var = f"{provider.upper()}_API_KEY"
            env_lines.append(f"{key_var}={info['api_key']}")
    
    with open(ENV_FILE, 'w') as f:
        f.write("\n".join(env_lines) + "\n")
    
    print(f"Generated .env with {len(vault)} keys")
    return True

if __name__ == "__main__":
    generate_env()
