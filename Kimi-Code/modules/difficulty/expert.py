"""
Kimi-Code: Expert Difficulty Tier
Complex problems requiring deep knowledge and tradeoff analysis.
"""
from typing import Dict, List

EXPERT_CHALLENGES = {
    "concepts": [
        "system_design", "advanced_algorithms", "optimization",
        "security_hardening", "distributed_systems", "performance_tuning",
        "advanced_concurrency", "custom_data_structures"
    ],
    "constraints": {
        "max_lines": 500,
        "max_functions": 20,
        "max_complexity": 12,
        "allowed_imports": ["all"],
        "time_limit_seconds": 1800
    },
    "evaluation_criteria": [
        "Optimal algorithmic complexity",
        "Production-ready code quality",
        "Comprehensive error handling",
        "Scalable architecture",
        "Security best practices"
    ],
    "hint_policy": {
        "hints_available": 2,
        "hint_penalty": 0.15,
        "first_hint_free": False
    },
    "xp_multiplier": 2.0,
    "unlock_requirements": {
        "global_level": 10,
        "prerequisites": ["journeyman_complete", "multiple_languages_unlocked"]
    }
}

def get_tier_config() -> Dict:
    return EXPERT_CHALLENGES
