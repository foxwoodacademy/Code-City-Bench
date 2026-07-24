"""
Kimi-Code: Journeyman Difficulty Tier
Intermediate challenges requiring design decisions.
"""
from typing import Dict, List

JOURNEYMAN_CHALLENGES = {
    "concepts": [
        "design_patterns", "recursion", "dynamic_programming_basics",
        "api_integration", "database_operations", "testing_strategies",
        "concurrency_basics", "memory_management"
    ],
    "constraints": {
        "max_lines": 200,
        "max_functions": 10,
        "max_complexity": 8,
        "allowed_imports": ["standard_library", "third_party"],
        "time_limit_seconds": 900
    },
    "evaluation_criteria": [
        "Appropriate design pattern usage",
        "Handles all edge cases gracefully",
        "Efficient time/space complexity",
        "Comprehensive test coverage",
        "Clean architecture"
    ],
    "hint_policy": {
        "hints_available": 3,
        "hint_penalty": 0.12,
        "first_hint_free": False
    },
    "xp_multiplier": 1.5,
    "unlock_requirements": {
        "global_level": 6,
        "prerequisites": ["apprentice_complete", "skill_tree_node_5"]
    }
}

def get_tier_config() -> Dict:
    return JOURNEYMAN_CHALLENGES
