"""
Kimi-Code: Red Hat Module
Intuition, gut feelings, and emotional intelligence challenges.
"""
from typing import Dict, List

RED_HAT_CHALLENGES = [
    {
        "id": "hat_red_001",
        "title": "🔥 Gut Reaction Assessment",
        "description": "Record your immediate emotional reaction to this code without analysis.",
        "code": "function processPayment(user, amount) {
    if (user.credit > amount) {
        user.credit -= amount;
        return true;
    }
    return false;
}
",
        "tasks": [
            "What's your immediate emotional reaction? (1 sentence)",
            "Does this code feel trustworthy? Rate 1-10",
            "What part makes you most nervous?",
            "Would you approve this for production based on gut feeling?"
        ],
        "expected": {
            "reaction": "Subjective but should mention floating point or race conditions",
            "trust_rating": "Typically 3-5 due to lack of validation",
            "nervous_part": "Direct mutation without validation",
            "production_approval": "No"
        },
        "difficulty": 2
    },
    {
        "id": "hat_red_002",
        "title": "🔥 Intuitive Bug Hunt",
        "description": "Without deep analysis, predict where bugs are most likely hiding.",
        "code": "class UserManager {
    constructor() {
        this.users = {};
    }
    addUser(id, data) {
        this.users[id] = data;
    }
    getUser(id) {
        return this.users[id];
    }
    deleteUser(id) {
        delete this.users[id];
    }
}
",
        "tasks": [
            "List 3 places your intuition says bugs hide",
            "Rate confidence for each prediction (1-10)",
            "What's the 'smell' that triggers your suspicion?",
            "Compare your gut predictions to actual analysis after"
        ],
        "expected": {
            "predictions": ["No validation on addUser", "No error handling in getUser", "Race conditions in concurrent access"],
            "confidence": "Typically 7-9 for missing validation",
            "smell": "No error handling, direct mutation",
            "accuracy_check": "Gut usually correct on validation issues"
        },
        "difficulty": 3
    }
]

def get_challenges(difficulty_range: tuple = None) -> List[Dict]:
    challenges = RED_HAT_CHALLENGES
    if difficulty_range:
        min_d, max_d = difficulty_range
        challenges = [c for c in challenges if min_d <= c["difficulty"] <= max_d]
    return challenges
