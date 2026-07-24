"""
Kimi-Code: Novice Difficulty Tier
Entry-level challenges focusing on fundamentals.
"""
from typing import Dict, List

NOVICE_CHALLENGES = {
    "concepts": [
        "variables", "data_types", "operators", "conditionals", 
        "loops", "functions", "arrays_lists", "basic_io"
    ],
    "constraints": {
        "max_lines": 50,
        "max_functions": 3,
        "max_complexity": 3,
        "allowed_imports": ["standard_library_only"],
        "time_limit_seconds": 300
    },
    "evaluation_criteria": [
        "Code runs without errors",
        "Output matches expected exactly",
        "Uses appropriate data types",
        "Follows naming conventions",
        "Includes basic comments"
    ],
    "hint_policy": {
        "hints_available": 5,
        "hint_penalty": 0.05,  # 5% score reduction per hint
        "first_hint_free": True
    },
    "xp_multiplier": 1.0,
    "unlock_requirements": {
        "global_level": 1,
        "prerequisites": []
    }
}

def get_tier_config() -> Dict:
    return NOVICE_CHALLENGES

def evaluate_novice_submission(code: str, output: str, expected: str, 
                                hints_used: int, time_taken: int) -> Dict:
    """Evaluate a novice-level submission."""
    score = 100

    # Correctness (60%)
    if output.strip() == expected.strip():
        correctness = 60
    else:
        correctness = 0

    # Code quality (20%)
    quality = 20
    if len(code.split('
')) > NOVICE_CHALLENGES["constraints"]["max_lines"]:
        quality -= 5
    if 'def ' not in code and 'function' not in code:
        quality -= 5  # Should use functions

    # Style (10%)
    style = 10
    if '#' not in code and '//' not in code:
        style -= 5  # Should have comments

    # Time bonus (10%)
    time_bonus = 10 if time_taken < 180 else 5

    score = correctness + quality + style + time_bonus

    # Hint penalty
    penalty = max(0, (hints_used - (1 if NOVICE_CHALLENGES["hint_policy"]["first_hint_free"] else 0)) 
                  * NOVICE_CHALLENGES["hint_policy"]["hint_penalty"] * 100)
    score = max(0, score - penalty)

    return {
        "score": round(score, 1),
        "passed": score >= 70,
        "grade": "S" if score >= 95 else "A" if score >= 85 else "B" if score >= 70 else "C" if score >= 50 else "D",
        "feedback": _generate_feedback(score, correctness, quality, style)
    }

def _generate_feedback(score: float, correctness: int, quality: int, style: int) -> str:
    if score >= 95:
        return "Perfect! You understand the basics completely."
    elif score >= 85:
        return f"Great work! Correctness: {correctness}/60, Quality: {quality}/20, Style: {style}/10"
    elif score >= 70:
        return f"Good effort. Focus on: {'output correctness' if correctness < 60 else 'code structure' if quality < 15 else 'comments and style'}"
    else:
        return "Review the fundamentals. Check your logic and syntax carefully."
