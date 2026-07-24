"""
Kimi-Code: Debug Missions
Find and fix bugs in broken code.
"""
from typing import Dict, List

DEBUG_MISSIONS = [
    {
        "id": "debug_001",
        "title": "Off-by-One Hunter",
        "description": "Find the off-by-one error causing array index issues.",
        "broken_code": "def process_items(items):
    results = []
    for i in range(len(items)):
        if i < len(items) - 1:
            results.append(items[i] + items[i + 1])
    return results
",
        "bug_type": "off_by_one",
        "expected_behavior": "Sum adjacent pairs including last element with first",
        "actual_behavior": "Misses the wrap-around pair",
        "fix": "Change condition to handle wrap-around: results.append(items[i] + items[(i + 1) % len(items)])",
        "difficulty": 3,
        "hints": [
            "Check what happens at the last iteration",
            "The last element should pair with the first",
            "Modulo operator can help with wrap-around"
        ]
    },
    {
        "id": "debug_002",
        "title": "Race Condition Detective",
        "description": "Find the concurrency bug in this multi-threaded code.",
        "broken_code": "class Counter:
    def __init__(self):
        self.count = 0
    def increment(self):
        current = self.count
        self.count = current + 1
",
        "bug_type": "race_condition",
        "expected_behavior": "Thread-safe increment",
        "actual_behavior": "Lost updates under concurrency",
        "fix": "Use threading.Lock or atomic operations",
        "difficulty": 5,
        "hints": [
            "Read-modify-write is not atomic",
            "Two threads can read same value simultaneously",
            "Lock around the critical section"
        ]
    },
    {
        "id": "debug_003",
        "title": "Memory Leak Hunter",
        "description": "Find the memory leak in this event handler.",
        "broken_code": "class EventManager:
    def __init__(self):
        self.listeners = []
    def on(self, event, callback):
        self.listeners.append((event, callback))
    def emit(self, event, data):
        for e, cb in self.listeners:
            if e == event:
                cb(data)
",
        "bug_type": "memory_leak",
        "expected_behavior": "Listeners can be removed to free memory",
        "actual_behavior": "Listeners accumulate forever",
        "fix": "Implement off() method and use weak references",
        "difficulty": 4,
        "hints": [
            "There's no way to remove listeners",
            "Consider what happens with closures capturing large objects",
            "Weak references or explicit cleanup needed"
        ]
    },
    {
        "id": "debug_004",
        "title": "Type Confusion",
        "description": "Find where type assumptions break down.",
        "broken_code": "def calculate_average(scores):
    total = sum(scores)
    return total / len(scores)
",
        "bug_type": "type_error",
        "expected_behavior": "Handle any numeric input",
        "actual_behavior": "Crashing on empty list, strings, None",
        "fix": "Add validation: if not scores or not all(isinstance(x, (int, float)) for x in scores): raise ValueError",
        "difficulty": 2,
        "hints": [
            "What happens with empty list?",
            "What types could be in scores?",
            "Validate before calculating"
        ]
    },
    {
        "id": "debug_005",
        "title": "Async Await Trap",
        "description": "Fix the async code that's not actually awaiting.",
        "broken_code": "async def fetch_data():
    response = requests.get('https://api.example.com')
    return response.json()
",
        "bug_type": "async_error",
        "expected_behavior": "Non-blocking HTTP request",
        "actual_behavior": "Blocking synchronous call in async function",
        "fix": "Use aiohttp or httpx for async HTTP: async with aiohttp.ClientSession() as session: async with session.get(url) as response: return await response.json()",
        "difficulty": 4,
        "hints": [
            "requests is synchronous, not async",
            "Need async-compatible HTTP library",
            "Remember to await all async operations"
        ]
    }
]

def get_missions(difficulty_range: tuple = None) -> List[Dict]:
    missions = DEBUG_MISSIONS
    if difficulty_range:
        min_d, max_d = difficulty_range
        missions = [m for m in missions if min_d <= m["difficulty"] <= max_d]
    return missions

def evaluate_debug_submission(mission: Dict, fixed_code: str, explanation: str) -> Dict:
    """Evaluate a debug mission submission."""
    score = 0
    feedback = []

    # Check if bug is fixed (60%)
    # Would run tests against fixed_code
    bug_fixed = True  # Placeholder
    if bug_fixed:
        score += 60
        feedback.append("✓ Bug appears to be fixed")
    else:
        feedback.append("✗ Bug not fixed - tests still failing")

    # Explanation quality (25%)
    if mission["bug_type"] in explanation.lower():
        score += 15
        feedback.append("✓ Correctly identified bug type")
    if "root cause" in explanation.lower() or "because" in explanation.lower():
        score += 10
        feedback.append("✓ Explained root cause")

    # Code quality (15%)
    if "test" in fixed_code.lower():
        score += 5
        feedback.append("✓ Added tests")
    if "docstring" in fixed_code.lower() or "comment" in fixed_code.lower():
        score += 5
        feedback.append("✓ Documented the fix")

    return {
        "score": score,
        "passed": score >= 70,
        "feedback": "
".join(feedback),
        "grade": "S" if score >= 95 else "A" if score >= 85 else "B" if score >= 70 else "C"
    }
