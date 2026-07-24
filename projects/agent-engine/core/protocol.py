# Swarm Communication Protocol
# Defines standardized message structures for agent-to-agent interactions.

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict
import uuid

class MessageType(Enum):
    TASK = "task"
    RESPONSE = "response"
    BROADCAST = "broadcast"
    ERROR = "error"

@dataclass
class SwarmMessage:
    """
    Standardized communication envelope for agents in the swarm.
    Ensures message traceability, type identification, and structured payload.
    """
    sender_id: str
    recipient_id: str
    message_type: MessageType
    payload: Dict[str, Any]
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=lambda: __import__('time').time())
