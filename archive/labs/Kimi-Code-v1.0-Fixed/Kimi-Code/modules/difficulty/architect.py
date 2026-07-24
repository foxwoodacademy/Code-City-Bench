"""
Kimi-Code: Architect Difficulty Tier
Design and lead complex systems. The pinnacle of Kimi-Code.
"""
from typing import Dict, List

ARCHITECT_CHALLENGES = {
    "concepts": [
        "enterprise_architecture", "platform_design", "organizational_scaling",
        "technical_strategy", "research_direction", "industry_influence",
        "legacy_modernization", "future_technology_adoption"
    ],
    "constraints": {
        "max_lines": None,  # No limit
        "max_functions": None,
        "max_complexity": None,
        "allowed_imports": ["all"],
        "time_limit_seconds": 7200  # 2 hours
    },
    "evaluation_criteria": [
        "System design at scale",
        "Business impact analysis",
        "Team enablement strategy",
        "Technology roadmap creation",
        "Industry thought leadership"
    ],
    "hint_policy": {
        "hints_available": 0,  # No hints at architect level
        "hint_penalty": 0,
        "first_hint_free": False
    },
    "xp_multiplier": 5.0,
    "unlock_requirements": {
        "global_level": 20,
        "prerequisites": ["master_complete", "all_hats_level_10", "skill_tree_90_percent"]
    }
}

def get_tier_config() -> Dict:
    return ARCHITECT_CHALLENGES
