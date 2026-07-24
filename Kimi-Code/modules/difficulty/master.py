"""
Kimi-Code: Master Difficulty Tier
Expert-level challenges requiring innovation and teaching ability.
"""
from typing import Dict, List

MASTER_CHALLENGES = {
    "concepts": [
        "language_design", "compiler_construction", "operating_systems",
        "database_internals", "network_protocols", "cryptography",
        "machine_learning_systems", "formal_verification"
    ],
    "constraints": {
        "max_lines": 1000,
        "max_functions": 50,
        "max_complexity": 15,
        "allowed_imports": ["all", "custom_libraries"],
        "time_limit_seconds": 3600
    },
    "evaluation_criteria": [
        "Novel solutions to hard problems",
        "Teaching ability (explain to others)",
        "Cross-domain knowledge application",
        "Mentoring quality feedback",
        "Architectural vision"
    ],
    "hint_policy": {
        "hints_available": 1,
        "hint_penalty": 0.20,
        "first_hint_free": False
    },
    "xp_multiplier": 3.0,
    "unlock_requirements": {
        "global_level": 15,
        "prerequisites": ["expert_complete", "hat_mastery_level_5"]
    }
}

def get_tier_config() -> Dict:
    return MASTER_CHALLENGES
