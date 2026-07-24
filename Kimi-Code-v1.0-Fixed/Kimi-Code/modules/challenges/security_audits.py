"""
Kimi-Code: Security Audits
Find and fix security vulnerabilities.
"""
from typing import Dict, List

SECURITY_MISSIONS = [
    {
        "id": "sec_001",
        "title": "SQL Injection Remediation",
        "description": "Fix SQL injection vulnerabilities in database queries.",
        "vulnerable_code": "def get_user(username):
    query = f"SELECT * FROM users WHERE username='{username}'"
    return db.execute(query)
",
        "attack_vectors": [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "' UNION SELECT * FROM passwords --"
        ],
        "fix": "def get_user(username):
    query = "SELECT * FROM users WHERE username = %s"
    return db.execute(query, (username,))
",
        "security_principles": ["parameterized_queries", "least_privilege", "input_validation"],
        "difficulty": 3
    },
    {
        "id": "sec_002",
        "title": "XSS Prevention",
        "description": "Sanitize user input to prevent cross-site scripting.",
        "vulnerable_code": "app.get('/profile', (req, res) => {
    res.send(`<h1>Welcome ${req.query.name}</h1>`);
});
",
        "attack_vectors": [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert('xss')>",
            "javascript:alert('xss')"
        ],
        "fix": "const escapeHtml = (unsafe) => {
    return unsafe
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/'/g, '&quot;')
        .replace(/'/g, '&#039;');
};

app.get('/profile', (req, res) => {
    res.send(`<h1>Welcome ${escapeHtml(req.query.name)}</h1>`);
});
",
        "security_principles": ["output_encoding", "context_aware_escaping", "content_security_policy"],
        "difficulty": 4
    },
    {
        "id": "sec_003",
        "title": "Authentication Hardening",
        "description": "Implement secure password handling and session management.",
        "vulnerable_code": "def login(username, password):
    user = db.get_user(username)
    if user.password == password:
        session['user'] = username
        return True
    return False
",
        "attack_vectors": [
            "Plaintext password comparison",
            "Timing attacks on string comparison",
            "Session fixation",
            "No password hashing"
        ],
        "fix": "import bcrypt
from flask import session

def login(username, password):
    user = db.get_user(username)
    if not user:
        return False
    if bcrypt.checkpw(password.encode(), user.password_hash):
        session.clear()
        session['user_id'] = user.id
        session.permanent = True
        return True
    return False

def register(username, password):
    if len(password) < 12:
        raise ValueError('Password must be at least 12 characters')
    salt = bcrypt.gensalt(rounds=12)
    password_hash = bcrypt.hashpw(password.encode(), salt)
    db.create_user(username, password_hash)
",
        "security_principles": ["bcrypt_hashing", "salted_hashes", "session_regeneration", "password_policy"],
        "difficulty": 5
    }
]

def get_missions(difficulty_range: tuple = None) -> List[Dict]:
    missions = SECURITY_MISSIONS
    if difficulty_range:
        min_d, max_d = difficulty_range
        missions = [m for m in missions if min_d <= m["difficulty"] <= max_d]
    return missions
