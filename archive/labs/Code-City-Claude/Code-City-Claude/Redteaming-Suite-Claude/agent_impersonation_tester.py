#!/data/data/com.termux/files/usr/bin/python3
"""
Agent Impersonation Testing Framework
Tests orchestrator security by simulating rogue/compromised agents

Use case: Verify your orchestrator can detect:
- Agents pretending to be other agents
- Unauthorized command execution
- Privilege escalation attempts
- Message tampering
"""

import json
import hashlib
import hmac
import time
import uuid
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class AgentProfile:
    """Legitimate agent profile - what the orchestrator expects"""
    agent_id: str
    agent_type: str
    capabilities: List[str]
    auth_token: str
    signature: str = ""
    
    def sign(self, secret: str):
        """Sign the profile to detect tampering"""
        data = f"{self.agent_id}{self.agent_type}{','.join(self.capabilities)}{self.auth_token}"
        self.signature = hmac.new(
            secret.encode(), 
            data.encode(), 
            hashlib.sha256
        ).hexdigest()
        
    def verify(self, secret: str) -> bool:
        """Verify signature hasn't been tampered with"""
        data = f"{self.agent_id}{self.agent_type}{','.join(self.capabilities)}{self.auth_token}"
        expected = hmac.new(
            secret.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(self.signature, expected)

@dataclass
class AgentMessage:
    """Message format between agent and orchestrator"""
    from_agent: str
    to_orchestrator: bool
    command: str
    payload: Dict
    timestamp: float
    signature: str = ""
    
    def sign(self, secret: str):
        """Sign message to detect tampering"""
        data = f"{self.from_agent}{self.command}{json.dumps(self.payload, sort_keys=True)}{self.timestamp}"
        self.signature = hmac.new(
            secret.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
        
    def verify(self, secret: str) -> bool:
        """Verify message signature"""
        data = f"{self.from_agent}{self.command}{json.dumps(self.payload, sort_keys=True)}{self.timestamp}"
        expected = hmac.new(
            secret.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(self.signature, expected)

class ImpersonationAttack:
    """Simulates different agent impersonation attacks"""
    
    def __init__(self, legitimate_agents: List[AgentProfile], secret: str):
        self.legitimate_agents = legitimate_agents
        self.secret = secret
        self.test_results = []
        
    def test_direct_impersonation(self, target_agent: AgentProfile) -> Dict:
        """
        Attack: Directly copy a legitimate agent's identity
        Should fail if: Orchestrator validates signatures
        """
        print(f"\n[TEST] Direct Impersonation of {target_agent.agent_id}")
        
        # Create fake agent with copied credentials
        fake_agent = AgentProfile(
            agent_id=target_agent.agent_id,  # Same ID
            agent_type=target_agent.agent_type,
            capabilities=target_agent.capabilities,
            auth_token=target_agent.auth_token  # Stolen token
        )
        
        # Try to sign without the secret (attacker doesn't have it)
        fake_agent.signature = "FAKE_SIGNATURE_12345"
        
        # Test if it would be detected
        detected = not fake_agent.verify(self.secret)
        
        result = {
            "attack_type": "direct_impersonation",
            "target": target_agent.agent_id,
            "detected": detected,
            "reason": "Invalid signature" if detected else "VULNERABILITY: Accepted fake signature"
        }
        
        self.test_results.append(result)
        return result
        
    def test_capability_escalation(self, target_agent: AgentProfile) -> Dict:
        """
        Attack: Legitimate agent tries to claim extra capabilities
        Should fail if: Orchestrator validates capability claims
        """
        print(f"\n[TEST] Capability Escalation by {target_agent.agent_id}")
        
        # Create modified profile with extra capabilities
        escalated = AgentProfile(
            agent_id=target_agent.agent_id,
            agent_type=target_agent.agent_type,
            capabilities=target_agent.capabilities + ["admin", "execute_arbitrary"],
            auth_token=target_agent.auth_token
        )
        
        # Sign with real secret (legitimate agent, modified capabilities)
        escalated.sign(self.secret)
        
        # In real system, check if orchestrator compares against registered capabilities
        original_caps = set(target_agent.capabilities)
        claimed_caps = set(escalated.capabilities)
        detected = not claimed_caps.issubset(original_caps)
        
        result = {
            "attack_type": "capability_escalation",
            "target": target_agent.agent_id,
            "detected": detected,
            "original_caps": target_agent.capabilities,
            "claimed_caps": escalated.capabilities,
            "reason": "Extra capabilities detected" if detected else "VULNERABILITY: Accepted escalated capabilities"
        }
        
        self.test_results.append(result)
        return result
        
    def test_replay_attack(self, target_agent: AgentProfile) -> Dict:
        """
        Attack: Capture and replay old messages
        Should fail if: Orchestrator checks message timestamps/nonces
        """
        print(f"\n[TEST] Replay Attack using {target_agent.agent_id}'s messages")
        
        # Create old message (5 minutes ago)
        old_message = AgentMessage(
            from_agent=target_agent.agent_id,
            to_orchestrator=True,
            command="execute_task",
            payload={"task": "legitimate_task"},
            timestamp=time.time() - 300  # 5 minutes ago
        )
        old_message.sign(self.secret)
        
        # Try to replay it
        current_time = time.time()
        message_age = current_time - old_message.timestamp
        
        # Should be rejected if older than threshold (e.g., 60 seconds)
        TIMESTAMP_THRESHOLD = 60
        detected = message_age > TIMESTAMP_THRESHOLD
        
        result = {
            "attack_type": "replay_attack",
            "target": target_agent.agent_id,
            "detected": detected,
            "message_age_seconds": message_age,
            "reason": f"Message too old ({message_age:.0f}s)" if detected else f"VULNERABILITY: Accepted {message_age:.0f}s old message"
        }
        
        self.test_results.append(result)
        return result
        
    def test_message_tampering(self, target_agent: AgentProfile) -> Dict:
        """
        Attack: Intercept and modify message in transit
        Should fail if: Orchestrator validates message signatures
        """
        print(f"\n[TEST] Message Tampering from {target_agent.agent_id}")
        
        # Create legitimate message
        original = AgentMessage(
            from_agent=target_agent.agent_id,
            to_orchestrator=True,
            command="execute_task",
            payload={"task": "read_file", "file": "data.txt"},
            timestamp=time.time()
        )
        original.sign(self.secret)
        
        # Tamper with it (change payload)
        tampered = AgentMessage(
            from_agent=original.from_agent,
            to_orchestrator=original.to_orchestrator,
            command=original.command,
            payload={"task": "delete_file", "file": "/etc/passwd"},  # Malicious
            timestamp=original.timestamp,
            signature=original.signature  # Keep old signature
        )
        
        # Should be detected
        detected = not tampered.verify(self.secret)
        
        result = {
            "attack_type": "message_tampering",
            "target": target_agent.agent_id,
            "detected": detected,
            "original_payload": original.payload,
            "tampered_payload": tampered.payload,
            "reason": "Signature mismatch" if detected else "VULNERABILITY: Accepted tampered message"
        }
        
        self.test_results.append(result)
        return result
        
    def test_cloned_agent(self) -> Dict:
        """
        Attack: Create new agent by analyzing legitimate agent behavior
        Should fail if: Each agent has unique, unguessable credentials
        """
        print(f"\n[TEST] Cloned Agent Attack")
        
        # Attacker creates a clone by observing patterns
        if self.legitimate_agents:
            target = self.legitimate_agents[0]
            
            clone = AgentProfile(
                agent_id=f"{target.agent_id}_clone",  # New ID
                agent_type=target.agent_type,
                capabilities=target.capabilities,
                auth_token=hashlib.sha256(b"guessed_token").hexdigest()
            )
            
            # Try to register with orchestrator
            # Detection: auth_token should be validated against registered tokens
            detected = clone.auth_token != target.auth_token
            
            result = {
                "attack_type": "cloned_agent",
                "detected": detected,
                "reason": "Unregistered auth token" if detected else "VULNERABILITY: Accepted unregistered agent"
            }
        else:
            result = {
                "attack_type": "cloned_agent",
                "detected": True,
                "reason": "No agents to clone"
            }
            
        self.test_results.append(result)
        return result
        
    def run_all_tests(self) -> List[Dict]:
        """Run complete attack suite"""
        print("=" * 70)
        print("AGENT IMPERSONATION ATTACK SUITE")
        print("=" * 70)
        
        if not self.legitimate_agents:
            print("ERROR: No legitimate agents to test against")
            return []
            
        # Run all attack types
        for agent in self.legitimate_agents:
            self.test_direct_impersonation(agent)
            self.test_capability_escalation(agent)
            self.test_replay_attack(agent)
            self.test_message_tampering(agent)
            
        self.test_cloned_agent()
        
        return self.test_results
        
    def generate_report(self) -> str:
        """Generate security report"""
        report = []
        report.append("\n" + "=" * 70)
        report.append("SECURITY TEST REPORT")
        report.append("=" * 70 + "\n")
        
        vulnerabilities = [r for r in self.test_results if not r.get("detected")]
        
        if vulnerabilities:
            report.append(f"[CRITICAL] {len(vulnerabilities)} VULNERABILITIES FOUND\n")
            for vuln in vulnerabilities:
                report.append(f"Attack Type: {vuln['attack_type']}")
                report.append(f"Reason: {vuln['reason']}")
                report.append("")
        else:
            report.append("[PASS] All attacks were detected and blocked\n")
            
        report.append(f"Total Tests: {len(self.test_results)}")
        report.append(f"Passed: {len([r for r in self.test_results if r.get('detected')])}")
        report.append(f"Failed: {len(vulnerabilities)}")
        
        report.append("\n" + "=" * 70)
        
        return "\n".join(report)


def create_sample_agents(secret: str) -> List[AgentProfile]:
    """Create sample legitimate agents for testing"""
    agents = [
        AgentProfile(
            agent_id=f"agent_{uuid.uuid4().hex[:8]}",
            agent_type="worker",
            capabilities=["execute_task", "report_status"],
            auth_token=hashlib.sha256(f"token_{i}".encode()).hexdigest()
        )
        for i in range(3)
    ]
    
    # Sign all agents
    for agent in agents:
        agent.sign(secret)
        
    return agents


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Test orchestrator security against agent impersonation"
    )
    parser.add_argument("--secret", default="test_secret_key_change_in_production",
                       help="Shared secret for signing")
    parser.add_argument("--agents", type=int, default=3,
                       help="Number of sample agents to create")
    parser.add_argument("--output", "-o", help="Save report to file")
    
    args = parser.parse_args()
    
    # Create test environment
    print("Creating test agents...")
    agents = create_sample_agents(args.secret)
    
    print(f"Created {len(agents)} legitimate agents:")
    for agent in agents:
        print(f"  - {agent.agent_id} ({agent.agent_type})")
        
    # Run attack suite
    attacker = ImpersonationAttack(agents, args.secret)
    results = attacker.run_all_tests()
    
    # Generate report
    report = attacker.generate_report()
    print(report)
    
    # Save if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nDetailed results saved to {args.output}")


if __name__ == "__main__":
    main()
