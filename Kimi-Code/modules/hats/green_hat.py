"""
Kimi-Code: Green Hat Module
Creativity, alternatives, and innovative solutions.
"""
from typing import Dict, List

GREEN_HAT_CHALLENGES = [
    {
        "id": "hat_green_001",
        "title": "🌱 Alternative Algorithms",
        "description": "Propose 3 completely different approaches to this problem.",
        "code": "# Find the most frequent element in an array
def most_frequent(arr):
    counts = {}
    for x in arr:
        counts[x] = counts.get(x, 0) + 1
    return max(counts, key=counts.get)
",
        "tasks": [
            "Approach 1: Sorting-based (different time/space tradeoff)",
            "Approach 2: Probabilistic (approximate but fast)",
            "Approach 3: Parallel/distributed (for massive datasets)",
            "Compare tradeoffs of all 4 approaches (including original)"
        ],
        "expected": {
            "sorting": "Sort then scan for longest run: O(n log n) time, O(1) space",
            "probabilistic": "Count-Min Sketch: O(1) time, O(1) space, approximate",
            "parallel": "MapReduce: O(n/k) per node, scalable to TB",
            "tradeoffs": {
                "original": "O(n) time, O(n) space, exact, single-threaded",
                "sorting": "O(n log n) time, O(1) space, exact, in-place",
                "probabilistic": "O(1) time, O(1) space, approximate, streaming",
                "parallel": "O(n/k) time, O(k) space, exact, distributed"
            }
        },
        "difficulty": 5
    },
    {
        "id": "hat_green_002",
        "title": "🌱 Feature Extension",
        "description": "Extend this basic logger into a comprehensive observability platform.",
        "code": "class Logger {
    log(level, message) {
        console.log(`[${level}] ${message}`);
    }
}
",
        "tasks": [
            "Design structured logging with JSON output",
            "Add distributed tracing correlation IDs",
            "Implement log aggregation pipeline",
            "Create automatic alerting on error patterns",
            "Design log-based metrics extraction"
        ],
        "expected": {
            "structured_logging": "JSON with timestamp, service, trace_id, span_id, severity",
            "tracing": "OpenTelemetry integration, context propagation",
            "aggregation": "Fluentd/Vector → Kafka → ClickHouse",
            "alerting": "Prometheus rules on error rate spikes",
            "metrics": "Extract request duration, error rate, throughput from logs"
        },
        "difficulty": 6
    },
    {
        "id": "hat_green_003",
        "title": "🌱 Language Translation",
        "description": "Translate this Python code to Rust, then to Go, then design a hybrid.",
        "code": "# Python: Dynamic, expressive
def process_data(items):
    return [x * 2 for x in items if x > 0]
",
        "tasks": [
            "Rust version: zero-cost abstractions, iterators",
            "Go version: explicit, simple, concurrent",
            "Hybrid design: Best of all three worlds",
            "Analyze when to use each approach"
        ],
        "expected": {
            "rust": "items.iter().filter(|&&x| x > 0).map(|x| x * 2).collect()",
            "go": "Explicit loop with append, easy to add goroutines",
            "hybrid": "Python for prototyping, Rust for performance-critical paths, Go for services",
            "when_to_use": {
                "python": "Rapid prototyping, data science, scripting",
                "rust": "Systems programming, safety-critical, performance",
                "go": "Microservices, cloud-native, team scalability"
            }
        },
        "difficulty": 5
    }
]

def get_challenges(difficulty_range: tuple = None) -> List[Dict]:
    challenges = GREEN_HAT_CHALLENGES
    if difficulty_range:
        min_d, max_d = difficulty_range
        challenges = [c for c in challenges if min_d <= c["difficulty"] <= max_d]
    return challenges
