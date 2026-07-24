"""
Kimi-Code: Black Hat Module
Risk assessment, security analysis, and devil's advocate challenges.
"""
from typing import Dict, List

BLACK_HAT_CHALLENGES = [
    {
        "id": "hat_black_001",
        "title": "⚠️ Security Vulnerability Hunt",
        "description": "Find and exploit every security vulnerability in this authentication code.",
        "code": "app.post('/login', (req, res) => {
    const { username, password } = req.body;
    const query = `SELECT * FROM users WHERE username='${username}'`;
    db.query(query, (err, results) => {
        if (results[0].password === password) {
            req.session.user = results[0];
            res.json({ success: true });
        }
    });
});
",
        "tasks": [
            "Identify SQL injection vector",
            "Find timing attack vulnerability",
            "Locate missing input validation",
            "Discover session fixation risk",
            "Propose fix for each vulnerability"
        ],
        "expected": {
            "sql_injection": "username: ' OR '1'='1",
            "timing_attack": "String comparison not constant-time",
            "missing_validation": "No length/type checks on username/password",
            "session_fixation": "Session not regenerated after login",
            "fixes": ["Parameterized queries", "bcrypt compare", "Joi validation", "req.session.regenerate()"]
        },
        "difficulty": 5
    },
    {
        "id": "hat_black_002",
        "title": "⚠️ Failure Mode Analysis",
        "description": "Analyze how this distributed system fails under various conditions.",
        "code": "// Service mesh with 3 services
// Service A → Service B → Service C → Database
// Each service has 99.9% uptime
// Timeout: 5s per hop
// Retry: 3 times with exponential backoff
",
        "tasks": [
            "Calculate overall system availability",
            "Identify cascade failure scenarios",
            "Find timeout amplification risks",
            "Analyze retry storm potential",
            "Design circuit breaker placement"
        ],
        "expected": {
            "availability": "~99.7% (0.999^3)",
            "cascade_scenarios": ["B fails → A retries amplify load", "DB slow → all services timeout"],
            "timeout_risk": "15s total latency if all timeouts hit",
            "retry_storm": "3 retries × 3 services = 9x load on failure",
            "circuit_breakers": ["Between A-B", "Between B-C", "Between C-DB"]
        },
        "difficulty": 7
    },
    {
        "id": "hat_black_003",
        "title": "⚠️ Edge Case Annihilation",
        "description": "Destroy this function with edge cases it doesn't handle.",
        "code": "def divide(a, b):
    return a / b
",
        "tasks": [
            "List 10 edge cases that break this function",
            "Categorize by severity (crash/data corruption/silent wrong)",
            "Write test cases for each edge case",
            "Propose robust implementation"
        ],
        "expected": {
            "edge_cases": [
                "b=0 (ZeroDivisionError)",
                "a=inf, b=inf (NaN)",
                "a=NaN (propagates NaN)",
                "b=very_small (overflow to inf)",
                "a=MAX_INT, b=0.5 (overflow)",
                "strings passed (TypeError)",
                "None passed (TypeError)",
                "complex numbers (TypeError)",
                "Negative zero (sign preservation)",
                "Denormalized floats (precision loss)"
            ],
            "severity": {
                "crash": ["ZeroDivisionError", "TypeError"],
                "silent_wrong": ["NaN propagation", "precision loss"],
                "data_corruption": ["overflow"]
            }
        },
        "difficulty": 4
    }
]

def get_challenges(difficulty_range: tuple = None) -> List[Dict]:
    challenges = BLACK_HAT_CHALLENGES
    if difficulty_range:
        min_d, max_d = difficulty_range
        challenges = [c for c in challenges if min_d <= c["difficulty"] <= max_d]
    return challenges
