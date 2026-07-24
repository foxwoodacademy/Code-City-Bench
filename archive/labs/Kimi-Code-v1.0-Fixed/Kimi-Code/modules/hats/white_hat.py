"""
Kimi-Code: White Hat Module
Objective facts, data analysis, and information gathering challenges.
"""
from typing import Dict, List

WHITE_HAT_CHALLENGES = [
    {
        "id": "hat_white_001",
        "title": "📊 Complexity Analysis",
        "description": "Analyze the time and space complexity of this algorithm objectively.",
        "code": "def find_pairs(arr, target):
    result = []
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] + arr[j] == target:
                result.append((arr[i], arr[j]))
    return result
",
        "tasks": [
            "State the exact time complexity in Big-O notation",
            "State the exact space complexity",
            "Identify the bottleneck operation",
            "Count the exact number of comparisons for input [1,2,3,4,5]"
        ],
        "expected": {
            "time_complexity": "O(n²)",
            "space_complexity": "O(k) where k is number of pairs",
            "bottleneck": "Nested loop comparison",
            "comparisons": "10"
        },
        "difficulty": 3
    },
    {
        "id": "hat_white_002",
        "title": "📊 Data Flow Mapping",
        "description": "Map the complete data flow through this microservice architecture.",
        "code": "// API Gateway → Auth Service → User Service → Database
//                    ↓
//              Cache (Redis)
//                    ↓
//              Notification Service → Queue (RabbitMQ)
",
        "tasks": [
            "List all data transformations at each step",
            "Identify synchronous vs asynchronous flows",
            "Map all external dependencies",
            "Document expected request/response formats"
        ],
        "expected": {
            "transformations": ["JWT validation", "User lookup", "Cache read/write", "Event publishing"],
            "sync_flows": ["Gateway→Auth→User→DB"],
            "async_flows": ["User→Cache", "User→Notification→Queue"],
            "dependencies": ["Redis", "PostgreSQL", "RabbitMQ"]
        },
        "difficulty": 5
    },
    {
        "id": "hat_white_003",
        "title": "📊 Dependency Inventory",
        "description": "Catalog all dependencies and their versions in this project.",
        "code": "// package.json excerpt
{
  "dependencies": {
    "express": "^4.18.0",
    "lodash": "^4.17.21",
    "axios": "^1.2.0"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "eslint": "^8.0.0"
  }
}
",
        "tasks": [
            "List all direct dependencies with exact versions",
            "Identify which are runtime vs development",
            "Check for known vulnerabilities (simulate)",
            "Calculate total transitive dependency count estimate"
        ],
        "expected": {
            "direct_runtime": ["express@4.18.0", "lodash@4.17.21", "axios@1.2.0"],
            "direct_dev": ["jest@29.0.0", "eslint@8.0.0"],
            "vulnerabilities": ["lodash@4.17.21 has prototype pollution CVE"],
            "transitive_estimate": "50-100"
        },
        "difficulty": 4
    }
]

def get_challenges(difficulty_range: tuple = None) -> List[Dict]:
    challenges = WHITE_HAT_CHALLENGES
    if difficulty_range:
        min_d, max_d = difficulty_range
        challenges = [c for c in challenges if min_d <= c["difficulty"] <= max_d]
    return challenges
