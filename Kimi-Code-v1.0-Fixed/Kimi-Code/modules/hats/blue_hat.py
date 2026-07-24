"""
Kimi-Code: Blue Hat Module
Meta-analysis, process management, and synthesis.
"""
from typing import Dict, List

BLUE_HAT_CHALLENGES = [
    {
        "id": "hat_blue_001",
        "title": "🧠 Process Review",
        "description": "Analyze the development process used to create this code.",
        "code": "// TODO: Add payment processing
// FIXME: Handle edge cases
// HACK: Working around API limitation
// NOTE: This needs refactoring before release

function processOrder(order) {
    // ... 200 lines of mixed concerns
}
",
        "tasks": [
            "Identify process smells from code comments",
            "Reconstruct likely development timeline",
            "Assess code review quality",
            "Design improved development process",
            "Create checklist to prevent these issues"
        ],
        "expected": {
            "process_smells": ["Tech debt accumulation", "No refactoring phase", "Missing tests"],
            "timeline": "Rushed MVP → Bug fixes → Never refactored",
            "review_quality": "Low - comments indicate known issues merged",
            "improved_process": "TDD → Implementation → Refactor → Review → Merge",
            "checklist": ["No TODO/FIXME in merged code", "All edge cases tested", "Single responsibility per function"]
        },
        "difficulty": 4
    },
    {
        "id": "hat_blue_002",
        "title": "🧠 Synthesis Exercise",
        "description": "Synthesize findings from all 5 other hats into an action plan.",
        "code": "// Given analysis from all 5 hats:
// White: O(n²) time, 3 external dependencies
// Red: Feels risky, trust level 4/10
// Black: SQL injection, no input validation
// Yellow: Clean structure, easy to extend
// Green: Could use caching, async processing
",
        "tasks": [
            "Prioritize all findings by impact/effort",
            "Create 30-60-90 day improvement plan",
            "Assign hat-focused responsibilities to team",
            "Design metrics to track improvement",
            "Schedule follow-up review"
        ],
        "expected": {
            "priorities": [
                "P0: Fix SQL injection (Black)",
                "P1: Add input validation (Black/White)",
                "P2: Implement caching (Green)",
                "P3: Add monitoring (White/Blue)",
                "P4: Refactor structure (Yellow/Green)"
            ],
            "30_day": "Security fixes, input validation, basic tests",
            "60_day": "Caching layer, async processing, monitoring",
            "90_day": "Full refactor, performance optimization, docs",
            "metrics": ["Security scan pass rate", "Test coverage %", "P95 latency", "Error rate"]
        },
        "difficulty": 6
    }
]

def get_challenges(difficulty_range: tuple = None) -> List[Dict]:
    challenges = BLUE_HAT_CHALLENGES
    if difficulty_range:
        min_d, max_d = difficulty_range
        challenges = [c for c in challenges if min_d <= c["difficulty"] <= max_d]
    return challenges
