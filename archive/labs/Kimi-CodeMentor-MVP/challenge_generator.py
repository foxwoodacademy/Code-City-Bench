
# Challenge Generator - creates adaptive challenges
challenge_generator_py = '''"""
Kimi-Code: Challenge Generator
Creates progressively difficult coding challenges across languages and hats.
"""
import random
import hashlib
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class Challenge:
    """Represents a coding challenge."""
    id: str
    title: str
    description: str
    language: str
    difficulty: int
    hat_focus: Optional[str]
    challenge_type: str
    track: str
    starter_code: str
    test_cases: List[Dict]
    hints: List[str]
    solution: str
    explanation: str
    xp_reward: int
    time_limit: int
    prerequisites: List[str]
    tags: List[str]

class ChallengeGenerator:
    """Generates and manages coding challenges."""
    
    CHALLENGE_TEMPLATES = {
        "python": {
            "basics": [
                {
                    "title": "Variable Detective",
                    "description": "Fix variable naming and type issues in this function.",
                    "type": "debug",
                    "starter": "def calc(x, y, z):\n    a = x + y\n    b = a * z\n    return b\n",
                    "issues": ["Poor naming", "Missing type hints", "No docstring"],
                    "difficulty_range": (1, 3)
                },
                {
                    "title": "List Comprehension Master",
                    "description": "Refactor this loop into a list comprehension.",
                    "type": "refactor",
                    "starter": "result = []\nfor i in range(100):\n    if i % 2 == 0:\n        result.append(i * 2)\n",
                    "difficulty_range": (2, 4)
                },
                {
                    "title": "Dictionary Deep Dive",
                    "description": "Implement a nested dictionary merge with conflict resolution.",
                    "type": "implementation",
                    "starter": "def merge_dicts(d1, d2):\n    # TODO: Implement merge\n    pass\n",
                    "difficulty_range": (3, 5)
                }
            ],
            "data_structures": [
                {
                    "title": "Custom Stack",
                    "description": "Implement a stack with O(1) min tracking.",
                    "type": "implementation",
                    "starter": "class MinStack:\n    def __init__(self):\n        pass\n    def push(self, val):\n        pass\n    def pop(self):\n        pass\n    def get_min(self):\n        pass\n",
                    "difficulty_range": (4, 6)
                },
                {
                    "title": "LRU Cache",
                    "description": "Implement an LRU cache with O(1) operations.",
                    "type": "implementation",
                    "starter": "class LRUCache:\n    def __init__(self, capacity):\n        self.capacity = capacity\n    def get(self, key):\n        pass\n    def put(self, key, value):\n        pass\n",
                    "difficulty_range": (6, 8)
                }
            ],
            "algorithms": [
                {
                    "title": "Binary Search Variants",
                    "description": "Implement lower_bound and upper_bound binary search.",
                    "type": "implementation",
                    "starter": "def lower_bound(arr, target):\n    # First index >= target\n    pass\n\ndef upper_bound(arr, target):\n    # First index > target\n    pass\n",
                    "difficulty_range": (5, 7)
                },
                {
                    "title": "Dynamic Programming Starter",
                    "description": "Solve the climbing stairs problem with memoization.",
                    "type": "implementation",
                    "starter": "def climb_stairs(n):\n    # Count ways to climb n stairs (1 or 2 steps at a time)\n    pass\n",
                    "difficulty_range": (4, 6)
                }
            ],
            "oop": [
                {
                    "title": "Design a Bank Account",
                    "description": "Implement a thread-safe bank account with transactions.",
                    "type": "design",
                    "starter": "class BankAccount:\n    def __init__(self, account_id):\n        pass\n    def deposit(self, amount):\n        pass\n    def withdraw(self, amount):\n        pass\n",
                    "difficulty_range": (5, 7)
                }
            ],
            "async": [
                {
                    "title": "Async Task Queue",
                    "description": "Implement a priority task queue with asyncio.",
                    "type": "implementation",
                    "starter": "import asyncio\n\nclass TaskQueue:\n    def __init__(self):\n        pass\n    async def add_task(self, coro, priority=0):\n        pass\n    async def run(self):\n        pass\n",
                    "difficulty_range": (7, 9)
                }
            ]
        },
        "javascript": {
            "basics": [
                {
                    "title": "Closure Fixer",
                    "description": "Fix closure issues in this loop-based code.",
                    "type": "debug",
                    "starter": "for (var i = 0; i < 5; i++) {\n    setTimeout(() => console.log(i), 100);\n}\n",
                    "difficulty_range": (2, 4)
                },
                {
                    "title": "Promise Chain",
                    "description": "Convert callback hell to clean async/await.",
                    "type": "refactor",
                    "starter": "getData(function(a) {\n    getMoreData(a, function(b) {\n        getMoreData(b, function(c) {\n            console.log(c);\n        });\n    });\n});\n",
                    "difficulty_range": (3, 5)
                }
            ],
            "dom": [
                {
                    "title": "Event Delegation",
                    "description": "Implement efficient event handling for dynamic lists.",
                    "type": "implementation",
                    "starter": "// Inefficient: attaches listener to each item\nitems.forEach(item => {\n    item.addEventListener('click', handleClick);\n});\n",
                    "difficulty_range": (4, 6)
                }
            ]
        },
        "rust": {
            "basics": [
                {
                    "title": "Ownership Transfer",
                    "description": "Fix ownership issues in this string manipulation code.",
                    "type": "debug",
                    "starter": "fn process(s: String) -> String {\n    let t = s;\n    s.push_str(\" world\");\n    t\n}\n",
                    "difficulty_range": (3, 5)
                }
            ]
        },
        "go": {
            "basics": [
                {
                    "title": "Goroutine Race",
                    "description": "Fix the race condition in this concurrent counter.",
                    "type": "debug",
                    "starter": "var counter int\n\nfunc increment() {\n    for i := 0; i < 1000; i++ {\n        counter++\n    }\n}\n\nfunc main() {\n    go increment()\n    go increment()\n    time.Sleep(time.Second)\n    fmt.Println(counter)\n}\n",
                    "difficulty_range": (4, 6)
                }
            ]
        }
    }
    
    HAT_CHALLENGES = {
        "white": {
            "title_prefix": "Analyze: ",
            "description_suffix": " Focus on objective facts and data flow.",
            "success_criteria": ["Correct complexity analysis", "Complete data flow mapping", "Accurate dependency list"]
        },
        "red": {
            "title_prefix": "Feel: ",
            "description_suffix": " Trust your gut. What's wrong here emotionally?",
            "success_criteria": ["Articulated gut reaction", "Identified intuitive red flags", "Honest trust assessment"]
        },
        "black": {
            "title_prefix": "Break: ",
            "description_suffix": " Find every way this could fail or be exploited.",
            "success_criteria": ["Found vulnerabilities", "Identified edge cases", "Listed failure modes"]
        },
        "yellow": {
            "title_prefix": "Celebrate: ",
            "description_suffix": " What's elegant and well-designed here?",
            "success_criteria": ["Identified strengths", "Found clever patterns", "Noted extensibility"]
        },
        "green": {
            "title_prefix": "Reimagine: ",
            "description_suffix": " Propose a completely different approach.",
            "success_criteria": ["Proposed alternative", "Suggested refactoring", "Applied design patterns"]
        },
        "blue": {
            "title_prefix": "Direct: ",
            "description_suffix": " Synthesize and create an action plan.",
            "success_criteria": ["Synthesized findings", "Created action plan", "Defined next steps"]
        }
    }
    
    def __init__(self, state_engine=None):
        self.state = state_engine
        self.challenge_cache = {}
    
    def generate_challenge(self, language: str, track: str, difficulty: int,
                          hat_focus: Optional[str] = None,
                          user_skills: Dict = None) -> Challenge:
        """Generate a challenge matching user level and focus."""
        
        # Get templates for language/track
        templates = self.CHALLENGE_TEMPLATES.get(language, {}).get(track, [])
        if not templates:
            templates = self._generate_generic_challenge(language, track, difficulty)
        
        # Filter by difficulty
        valid_templates = [
            t for t in templates
            if t["difficulty_range"][0] <= difficulty <= t["difficulty_range"][1]
        ]
        
        if not valid_templates:
            valid_templates = templates  # Fallback
        
        template = random.choice(valid_templates)
        
        # Apply hat modifications if specified
        if hat_focus:
            template = self._apply_hat_modifications(template, hat_focus)
        
        # Generate challenge ID
        challenge_id = hashlib.sha256(
            f"{language}:{track}:{difficulty}:{random.random()}".encode()
        ).hexdigest()[:12]
        
        # Calculate rewards
        xp = difficulty * 25
        time_limit = difficulty * 90  # seconds
        
        # Generate test cases
        test_cases = self._generate_test_cases(template, language)
        
        # Generate hints (progressive disclosure)
        hints = self._generate_hints(template, difficulty)
        
        return Challenge(
            id=challenge_id,
            title=template["title"],
            description=template["description"],
            language=language,
            difficulty=difficulty,
            hat_focus=hat_focus,
            challenge_type=template["type"],
            track=track,
            starter_code=template.get("starter", "# TODO: Implement"),
            test_cases=test_cases,
            hints=hints,
            solution=template.get("solution", "# Solution not available"),
            explanation=template.get("explanation", "# Explanation not available"),
            xp_reward=xp,
            time_limit=time_limit,
            prerequisites=template.get("prerequisites", []),
            tags=template.get("tags", [language, track, template["type"]])
        )
    
    def _generate_generic_challenge(self, language: str, track: str, 
                                    difficulty: int) -> List[Dict]:
        """Generate a generic challenge when no template exists."""
        return [{
            "title": f"{track.title()} Challenge",
            "description": f"Complete a {difficulty}/15 difficulty challenge in {language}.",
            "type": "implementation",
            "starter": f"# TODO: Implement solution in {language}\n",
            "difficulty_range": (difficulty, difficulty),
            "tags": [language, track]
        }]
    
    def _apply_hat_modifications(self, template: Dict, hat: str) -> Dict:
        """Modify challenge for Six Thinking Hats focus."""
        modified = template.copy()
        hat_config = self.HAT_CHALLENGES.get(hat, {})
        
        if "title_prefix" in hat_config:
            modified["title"] = hat_config["title_prefix"] + modified["title"]
        
        if "description_suffix" in hat_config:
            modified["description"] += hat_config["description_suffix"]
        
        if "success_criteria" in hat_config:
            modified["success_criteria"] = hat_config["success_criteria"]
        
        return modified
    
    def _generate_test_cases(self, template: Dict, language: str) -> List[Dict]:
        """Generate test cases for a challenge."""
        # This would be expanded with actual test generation logic
        return [
            {
                "input": "default",
                "expected": "correct",
                "description": "Basic functionality test"
            },
            {
                "input": "edge",
                "expected": "handled",
                "description": "Edge case test"
            }
        ]
    
    def _generate_hints(self, template: Dict, difficulty: int) -> List[str]:
        """Generate progressive hints."""
        base_hints = template.get("hints", [])
        
        if not base_hints:
            # Generate generic hints based on difficulty
            if difficulty <= 3:
                base_hints = [
                    "Read the code carefully and identify the main issue.",
                    "Check variable names and types.",
                    "Look for missing error handling."
                ]
            elif difficulty <= 6:
                base_hints = [
                    "Consider time/space complexity implications.",
                    "Think about edge cases and boundary conditions.",
                    "Review the algorithm choice - is there a better approach?"
                ]
            else:
                base_hints = [
                    "Analyze the architectural pattern being used.",
                    "Consider concurrency and thread safety.",
                    "Evaluate memory management and resource cleanup.",
                    "Think about scalability and performance at scale."
                ]
        
        return base_hints[:max(1, difficulty // 2)]
    
    def get_challenge_sequence(self, language: str, track: str, 
                               count: int = 5, difficulty_range: Tuple[int, int] = None,
                               hats_mode: bool = False) -> List[Challenge]:
        """Generate a sequence of challenges with progressive difficulty."""
        if difficulty_range:
            min_d, max_d = difficulty_range
        else:
            min_d, max_d = 1, 5
        
        challenges = []
        hats = ["white", "red", "black", "yellow", "green", "blue"] if hats_mode else [None]
        
        for i in range(count):
            # Progressive difficulty
            progress = i / max(count - 1, 1)
            difficulty = int(min_d + (max_d - min_d) * progress)
            
            # Rotate hats if in hats mode
            hat = hats[i % len(hats)] if hats_mode else None
            
            challenge = self.generate_challenge(language, track, difficulty, hat)
            challenges.append(challenge)
        
        return challenges
    
    def evaluate_submission(self, challenge: Challenge, submission: str,
                         time_taken: int, hints_used: int) -> Dict:
        """Evaluate a challenge submission."""
        # This would integrate with test runners
        # For now, return a structured evaluation framework
        
        success = True  # Would be determined by test results
        
        # Calculate score components
        base_score = 100
        time_penalty = max(0, (time_taken - challenge.time_limit) / challenge.time_limit * 20)
        hint_penalty = hints_used * 10
        
        final_score = max(0, base_score - time_penalty - hint_penalty)
        
        # Determine grade
        if final_score >= 95:
            grade = "S"
        elif final_score >= 85:
            grade = "A"
        elif final_score >= 70:
            grade = "B"
        elif final_score >= 50:
            grade = "C"
        else:
            grade = "D"
            success = False
        
        return {
            "success": success,
            "score": round(final_score, 1),
            "grade": grade,
            "time_taken": time_taken,
            "hints_used": hints_used,
            "xp_earned": challenge.xp_reward if success else challenge.xp_reward // 4,
            "feedback": self._generate_feedback(challenge, final_score, time_taken)
        }
    
    def _generate_feedback(self, challenge: Challenge, score: float, 
                          time_taken: int) -> str:
        """Generate personalized feedback."""
        if score >= 95:
            return "Outstanding! Your solution is elegant and efficient."
        elif score >= 85:
            return "Great work! Minor optimizations possible."
        elif score >= 70:
            return "Good effort. Review the suggested improvements."
        elif score >= 50:
            return "Passing, but significant issues remain. Study the solution."
        else:
            return "Keep practicing! Focus on understanding the fundamentals first."
'''

with open(f"{base_dir}/core/challenge_generator.py", 'w') as f:
    f.write(challenge_generator_py)

print("✅ challenge_generator.py written")