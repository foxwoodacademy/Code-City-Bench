"""
Kimi-Code: Apprentice Difficulty Tier
Building on basics with more complex logic and structures.
"""
from typing import Dict, List

APPRENTICE_CHALLENGES = {
    "concepts": [
        "nested_loops", "string_manipulation", "basic_algorithms",
        "file_handling", "error_handling_basics", "simple_classes",
        "list_comprehensions", "dictionary_operations"
    ],
    "constraints": {
        "max_lines": 100,
        "max_functions": 5,
        "max_complexity": 5,
        "allowed_imports": ["standard_library", "common_utils"],
        "time_limit_seconds": 600
    },
    "evaluation_criteria": [
        "Handles edge cases",
        "Efficient algorithm choice",
        "Proper error handling",
        "Clean code structure",
        "Appropriate data structures"
    ],
    "hint_policy": {
        "hints_available": 4,
        "hint_penalty": 0.08,
        "first_hint_free": False
    },
    "xp_multiplier": 1.2,
    "unlock_requirements": {
        "global_level": 3,
        "prerequisites": ["novice_basics_complete"]
    }
}

def get_tier_config() -> Dict:
    return APPRENTICE_CHALLENGES

def evaluate_apprentice_submission(code: str, test_results: List[bool],
                                    edge_cases_passed: int, total_edge_cases: int,
                                    hints_used: int, time_taken: int) -> Dict:
    score = 100

    # Test cases (50%)
    test_score = sum(test_results) / len(test_results) * 50 if test_results else 0

    # Edge cases (20%)
    edge_score = (edge_cases_passed / total_edge_cases * 20) if total_edge_cases else 20

    # Code quality (15%)
    quality = 15
    if 'try' not in code and 'except' not in code and 'if' not in code:
        quality -= 5  # Should have some error handling
    if len(code.split('
')) > APPRENTICE_CHALLENGES["constraints"]["max_lines"]:
        quality -= 5

    # Efficiency (10%)
    efficiency = 10
    # Would check for O(n²) when O(n) possible, etc.

    # Time bonus (5%)
    time_bonus = 5 if time_taken < 300 else 2

    score = test_score + edge_score + quality + efficiency + time_bonus
    penalty = hints_used * APPRENTICE_CHALLENGES["hint_policy"]["hint_penalty"] * 100
    score = max(0, score - penalty)

    return {
        "score": round(score, 1),
        "passed": score >= 75,
        "grade": "S" if score >= 95 else "A" if score >= 85 else "B" if score >= 75 else "C" if score >= 60 else "D",
        "breakdown": {
            "tests": round(test_score, 1),
            "edge_cases": round(edge_score, 1),
            "quality": quality,
            "efficiency": efficiency
        }
    }
