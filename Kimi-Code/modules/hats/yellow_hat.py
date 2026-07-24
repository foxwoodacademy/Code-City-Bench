"""
Kimi-Code: Yellow Hat Module
Benefits, value identification, and optimistic analysis.
"""
from typing import Dict, List

YELLOW_HAT_CHALLENGES = [
    {
        "id": "hat_yellow_001",
        "title": "✨ Pattern Recognition",
        "description": "Identify all clever patterns and design decisions in this code.",
        "code": "class EventEmitter {
    constructor() {
        this.events = new Map();
        this.maxListeners = 10;
    }
    
    on(event, listener) {
        if (!this.events.has(event)) {
            this.events.set(event, []);
        }
        const listeners = this.events.get(event);
        if (listeners.length >= this.maxListeners) {
            console.warn('Max listeners exceeded');
        }
        listeners.push(listener);
        return () => this.off(event, listener);
    }
    
    emit(event, ...args) {
        const listeners = this.events.get(event) || [];
        listeners.forEach(fn => fn(...args));
    }
}
",
        "tasks": [
            "List 5 positive design decisions",
            "Identify extensibility points",
            "Note performance optimizations",
            "Recognize developer experience improvements",
            "Suggest what makes this exemplary code"
        ],
        "expected": {
            "design_decisions": [
                "Map instead of object for key safety",
                "Max listeners prevents memory leaks",
                "Returns unsubscribe function",
                "Rest parameters for flexible args",
                "Defensive programming with fallback array"
            ],
            "extensibility": ["Easy to add once(), prependListener()", "Can extend with async support"],
            "performance": ["O(1) event lookup with Map", "No array allocation if no listeners"],
            "dx": ["Unsubscribe return", "Warning on leak", "Simple API"]
        },
        "difficulty": 3
    },
    {
        "id": "hat_yellow_002",
        "title": "✨ Value Extraction",
        "description": "Extract maximum learning value from this 'bad' code.",
        "code": "// Intentionally inefficient bubble sort
function sort(arr) {
    for (let i = 0; i < arr.length; i++) {
        for (let j = 0; j < arr.length; j++) {
            if (arr[j] > arr[j + 1]) {
                let temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
    return arr;
}
",
        "tasks": [
            "What algorithm concepts does this demonstrate well?",
            "How could this be a teaching tool?",
            "What positive habits are shown despite inefficiency?",
            "How does this illustrate Big-O visually?",
            "Transform this into a learning exercise"
        ],
        "expected": {
            "concepts": ["Comparison-based sorting", "In-place swapping", "Nested iteration pattern"],
            "teaching_value": ["Clear visualization of O(n²)", "Basis for understanding optimizations"],
            "positive_habits": ["Mutates input (intentional choice)", "Returns array for chaining", "Simple variable names"],
            "learning_exercise": "Have students optimize: add early exit flag, reduce inner loop range"
        },
        "difficulty": 3
    }
]

def get_challenges(difficulty_range: tuple = None) -> List[Dict]:
    challenges = YELLOW_HAT_CHALLENGES
    if difficulty_range:
        min_d, max_d = difficulty_range
        challenges = [c for c in challenges if min_d <= c["difficulty"] <= max_d]
    return challenges
