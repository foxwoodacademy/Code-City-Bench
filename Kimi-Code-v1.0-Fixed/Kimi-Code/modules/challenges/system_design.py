"""
Kimi-Code: System Design Challenges
Design scalable distributed systems.
"""
from typing import Dict, List

SYSTEM_DESIGNS = [
    {
        "id": "sysdesign_001",
        "title": "URL Shortener",
        "description": "Design a URL shortening service like bit.ly",
        "requirements": [
            "Generate unique short URLs",
            "Redirect to original URL",
            "Handle 10M requests/day",
            "99.9% uptime",
            "Analytics on clicks"
        ],
        "components": ["API Gateway", "Shortening Service", "Database", "Cache", "Analytics Pipeline"],
        "key_decisions": [
            "Base62 encoding for short IDs",
            "Consistent hashing for distributed storage",
            "Redis for hot URL cache",
            "Kafka for analytics events"
        ],
        "difficulty": 5
    },
    {
        "id": "sysdesign_002",
        "title": "Rate Limiter",
        "description": "Design a distributed rate limiter",
        "requirements": [
            "1000 requests/minute per user",
            "Distributed across 10 servers",
            "Minimal latency overhead",
            "Configurable limits per endpoint"
        ],
        "algorithms": ["Token Bucket", "Sliding Window Log", "Sliding Window Counter"],
        "implementation": {
            "token_bucket": "Tokens added at fixed rate, request consumes token",
            "sliding_window": "Track timestamps in Redis sorted set",
            "distributed": "Redis + Lua script for atomic operations"
        },
        "difficulty": 6
    },
    {
        "id": "sysdesign_003",
        "title": "Real-time Chat",
        "description": "Design WhatsApp/Slack-like messaging",
        "requirements": [
            "1M concurrent connections",
            "Message delivery within 100ms",
            "Offline message persistence",
            "End-to-end encryption",
            "Group chats up to 1000 users"
        ],
        "architecture": {
            "gateway": "WebSocket load balancer",
            "presence": "Redis for online status",
            "messaging": "Kafka for message queue",
            "storage": "Cassandra for message history",
            "push": "FCM/APNs for offline delivery"
        },
        "difficulty": 7
    }
]

def get_challenges(difficulty_range: tuple = None) -> List[Dict]:
    designs = SYSTEM_DESIGNS
    if difficulty_range:
        min_d, max_d = difficulty_range
        designs = [d for d in designs if min_d <= d["difficulty"] <= max_d]
    return designs
