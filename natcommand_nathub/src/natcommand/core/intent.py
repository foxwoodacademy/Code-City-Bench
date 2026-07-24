"""
Intent - The fundamental semantic unit for NatCommand.
Captures the 'vibe' and the desired 'action' from natural language.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any

@dataclass
class Intent:
    raw_input: str
    action: str  # e.g., 'save', 'sync', 'revert'
    nuance: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "raw": self.raw_input,
            "action": self.action,
            "nuance": self.nuance,
            "ts": self.timestamp
        }
