#!/usr/bin/env python3
"""
MotherBrain Swarm Persona Morphing Engine - Secure Tiered Edition
Enforces strict boundary access restrictions across public, internal, and administrative tiers.
Path: /storage/emulated/0/RootBase/data/motherbrain/api/persona_engine.py
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional

PERSONA_ROOT = Path("/storage/emulated/0/RootBase/data/motherbrain/api/personas")

class TieredPersonaEngine:
    def __init__(self):
        self.tiers = {
            1: PERSONA_ROOT / "tier1_public",
            2: PERSONA_ROOT / "tier2_internal",
            3: PERSONA_ROOT / "tier3_restricted"
        }
        for path in self.tiers.values():
            path.mkdir(parents=True, exist_ok=True)

    def locate_persona_file(self, persona_id: str) -> Optional[Path]:
        """Scans across all tier directories to find where the profile is stored."""
        filename = f"{persona_id.lower().strip()}.json"
        for tier_path in self.tiers.values():
            target = tier_path / filename
            if target.exists():
                return target
        return None

    def load_persona(self, persona_id: str, caller_tier: int = 1) -> Optional[Dict]:
        """Loads a profile only if the caller's tier level matches or exceeds the profile's tier restriction."""
        file_path = self.locate_persona_file(persona_id)
        if not file_path:
            return None

        try:
            with open(file_path, "r") as f:
                profile = json.load(f)
                
            # Enforcement Gate: If caller's clearance is lower than target tier, deny access
            if caller_tier < profile.get("tier", 1):
                return {"error": "ACCESS_DENIED", "msg": f"Security clearance insufficient for Tier {profile.get('tier')}"}
                
            return profile
        except Exception:
            return None

    def inject_persona_lens(self, base_prompt: str, persona_id: str, caller_tier: int = 1) -> str:
        """Applies a persona behavior layer if access authorization passes."""
        profile = self.load_persona(persona_id, caller_tier)
        if not profile or "error" in profile:
            # If access is denied, strip persona influence and return a restricted enforcement notice
            return f"[SECURITY RESTRICTION]: Axis to persona '{persona_id}' rejected or unauthorized."
            
        return (
            f"Adopt identity: [{profile['display_name']}] (Tier {profile['tier']})\n"
            f"BIAS MAP: {profile['system_bias']}\n\n"
            f"Execute objective: '{base_prompt}'"
        )

if __name__ == "__main__":
    engine = TieredPersonaEngine()
    print("🔒 Tiered Engine Online. Operational Verification Tests:")
    
    # Test 1: User trying to load an onboarding tool (Tier 1 access to Tier 1 persona) -> Allowed
    print("  - Public Calling Askhole:", "Allowed" if "error" not in str(engine.load_persona("askhole", caller_tier=1)) else "Denied")
    
    # Test 2: External loop trying to load the legal registry (Tier 1 access to Tier 3 persona) -> Denied
    print("  - Public Calling EquiLex:", "Allowed" if "error" not in str(engine.load_persona("equilex", caller_tier=1)) else "Blocked (Unauthorized access protected)")
