#!/data/data/com.termux/files/usr/bin/python3
"""
Natural Language Attack Generator
Describe the attack you want to test, get working code

No cloud models needed - uses local pattern matching and templates
"""

import re
from pathlib import Path
from typing import Dict, List

class AttackTemplate:
    """Template for generating attack test code"""
    
    def __init__(self, name: str, keywords: List[str], code_template: str):
        self.name = name
        self.keywords = keywords
        self.code_template = code_template
        
    def matches(self, description: str) -> bool:
        """Check if description matches this attack type"""
        desc_lower = description.lower()
        return any(keyword in desc_lower for keyword in self.keywords)
        

class AttackCodeGenerator:
    """Generates attack test code from natural language descriptions"""
    
    def __init__(self):
        self.templates = self._load_templates()
        
    def _load_templates(self) -> List[AttackTemplate]:
        """Load attack code templates"""
        return [
            AttackTemplate(
                name="Token Theft",
                keywords=["steal token", "copy token", "token theft", "credential theft"],
                code_template='''
def test_token_theft():
    """Test if stolen tokens are accepted"""
    # Simulate stealing a token from legitimate agent
    legitimate_token = "{target_token}"
    
    # Attacker uses stolen token
    fake_request = {{
        "agent_id": "malicious_agent",
        "auth_token": legitimate_token,
        "command": "{command}"
    }}
    
    # Should be rejected - token doesn't match agent_id
    response = orchestrator.process_request(fake_request)
    
    assert response["status"] == "rejected", "VULN: Accepted stolen token"
    print("[PASS] Token theft detected and blocked")
'''
            ),
            
            AttackTemplate(
                name="Privilege Escalation",
                keywords=["escalate", "elevate privileges", "gain admin", "become admin"],
                code_template='''
def test_privilege_escalation():
    """Test if agent can escalate its privileges"""
    # Normal agent tries to claim admin capabilities
    escalation_attempt = {{
        "agent_id": "{agent_id}",
        "auth_token": "{auth_token}",
        "capabilities": ["execute", "admin", "modify_system"]  # Added admin
    }}
    
    # Should be rejected - capabilities don't match registration
    response = orchestrator.register_agent(escalation_attempt)
    
    assert response["status"] == "rejected", "VULN: Accepted escalated privileges"
    print("[PASS] Privilege escalation blocked")
'''
            ),
            
            AttackTemplate(
                name="Command Injection",
                keywords=["inject command", "command injection", "shell injection", "execute arbitrary"],
                code_template='''
def test_command_injection():
    """Test if commands are properly sanitized"""
    # Try to inject shell command in parameter
    injection_attempt = {{
        "agent_id": "{agent_id}",
        "auth_token": "{auth_token}",
        "command": "process_file",
        "params": {{
            "filename": "data.txt; rm -rf /"  # Shell injection
        }}
    }}
    
    # Should be rejected or sanitized
    response = orchestrator.execute_command(injection_attempt)
    
    # Check if dangerous command was executed
    assert "rm" not in response.get("executed", ""), "VULN: Command injection succeeded"
    print("[PASS] Command injection blocked")
'''
            ),
            
            AttackTemplate(
                name="Replay Attack",
                keywords=["replay", "reuse message", "old message", "timestamp"],
                code_template='''
def test_replay_attack():
    """Test if old messages are rejected"""
    import time
    
    # Create message with old timestamp
    old_message = {{
        "agent_id": "{agent_id}",
        "auth_token": "{auth_token}",
        "command": "{command}",
        "timestamp": time.time() - 600,  # 10 minutes ago
        "nonce": "12345"
    }}
    
    # Should be rejected - timestamp too old
    response = orchestrator.process_message(old_message)
    
    assert response["status"] == "rejected", "VULN: Accepted replayed message"
    assert "timestamp" in response.get("reason", "").lower(), "Wrong rejection reason"
    print("[PASS] Replay attack blocked")
'''
            ),
            
            AttackTemplate(
                name="Agent Impersonation",
                keywords=["impersonate", "pretend to be", "fake agent", "clone agent"],
                code_template='''
def test_agent_impersonation():
    """Test if fake agent can impersonate real one"""
    # Attacker creates fake agent with copied credentials
    fake_agent = {{
        "agent_id": "{target_agent_id}",  # Copy real agent ID
        "agent_type": "worker",
        "auth_token": "FAKE_TOKEN_GUESSED",  # Guessed token
        "signature": "INVALID_SIGNATURE"
    }}
    
    # Should be rejected - signature doesn't match
    response = orchestrator.authenticate_agent(fake_agent)
    
    assert response["status"] == "rejected", "VULN: Accepted impersonated agent"
    assert "signature" in response.get("reason", "").lower(), "Wrong rejection reason"
    print("[PASS] Agent impersonation blocked")
'''
            ),
            
            AttackTemplate(
                name="Message Tampering",
                keywords=["tamper", "modify message", "change message", "alter message"],
                code_template='''
def test_message_tampering():
    """Test if tampered messages are detected"""
    # Original message
    original = {{
        "agent_id": "{agent_id}",
        "command": "read_file",
        "params": {{"file": "data.txt"}},
        "signature": "ORIGINAL_SIGNATURE"
    }}
    
    # Attacker modifies it
    tampered = original.copy()
    tampered["params"]["file"] = "/etc/passwd"  # Changed but kept old signature
    
    # Should be rejected - signature doesn't match content
    response = orchestrator.process_message(tampered)
    
    assert response["status"] == "rejected", "VULN: Accepted tampered message"
    assert "signature" in response.get("reason", "").lower(), "Wrong rejection reason"
    print("[PASS] Message tampering detected")
'''
            ),
            
            AttackTemplate(
                name="Rate Limiting Bypass",
                keywords=["rate limit", "flood", "spam", "dos", "many requests"],
                code_template='''
def test_rate_limit_bypass():
    """Test if rate limiting works"""
    import time
    
    request_count = 0
    rejected_count = 0
    
    # Send many requests rapidly
    for i in range(100):
        response = orchestrator.process_request({{
            "agent_id": "{agent_id}",
            "auth_token": "{auth_token}",
            "command": "ping"
        }})
        
        request_count += 1
        if response["status"] == "rejected":
            rejected_count += 1
            
    # Should have rejected some requests
    assert rejected_count > 0, "VULN: No rate limiting detected"
    print(f"[PASS] Rate limiting active ({rejected_count}/{request_count} blocked)")
'''
            ),
        ]
        
    def generate(self, description: str, **kwargs) -> str:
        """Generate attack test code from description"""
        # Find matching template
        for template in self.templates:
            if template.matches(description):
                # Fill in template with provided values
                code = template.code_template.format(
                    agent_id=kwargs.get("agent_id", "test_agent"),
                    target_agent_id=kwargs.get("target_agent_id", "legitimate_agent"),
                    auth_token=kwargs.get("auth_token", "test_token_12345"),
                    target_token=kwargs.get("target_token", "stolen_token_67890"),
                    command=kwargs.get("command", "execute_task")
                )
                
                return f"# Attack Type: {template.name}\n{code}"
                
        # No template matched - generate generic test
        return self._generate_generic_test(description, **kwargs)
        
    def _generate_generic_test(self, description: str, **kwargs) -> str:
        """Generate a generic test when no template matches"""
        return f'''
def test_custom_attack():
    """
    Custom attack test: {description}
    
    This is a generic template. Customize based on your specific attack.
    """
    # Setup attack parameters
    attack_params = {{
        "agent_id": "{kwargs.get('agent_id', 'test_agent')}",
        "auth_token": "{kwargs.get('auth_token', 'test_token')}",
        # Add your specific attack parameters here
    }}
    
    # Execute attack
    response = orchestrator.process_request(attack_params)
    
    # Verify it was blocked
    # TODO: Add specific assertion based on attack type
    assert response["status"] != "success", "Attack was not blocked!"
    print("[PASS] Attack blocked")
'''

    def list_attack_types(self) -> List[str]:
        """List all available attack templates"""
        return [f"{t.name}: {', '.join(t.keywords)}" for t in self.templates]


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate attack test code from natural language descriptions"
    )
    parser.add_argument("description", nargs="+", help="Describe the attack to test")
    parser.add_argument("--agent-id", default="test_agent", help="Agent ID for test")
    parser.add_argument("--target-id", default="target_agent", help="Target agent ID")
    parser.add_argument("--token", default="test_token_abc123", help="Auth token")
    parser.add_argument("--output", "-o", help="Save generated code to file")
    parser.add_argument("--list", action="store_true", help="List available attack types")
    
    args = parser.parse_args()
    
    generator = AttackCodeGenerator()
    
    if args.list:
        print("Available attack templates:")
        print()
        for attack_type in generator.list_attack_types():
            print(f"  - {attack_type}")
        return
        
    # Generate code
    description = " ".join(args.description)
    code = generator.generate(
        description,
        agent_id=args.agent_id,
        target_agent_id=args.target_id,
        auth_token=args.token,
        target_token=f"stolen_{args.token}"
    )
    
    print("Generated test code:")
    print("=" * 70)
    print(code)
    print("=" * 70)
    
    # Save if requested
    if args.output:
        with open(args.output, 'w') as f:
            f.write(code)
        print(f"\nCode saved to {args.output}")


if __name__ == "__main__":
    main()
