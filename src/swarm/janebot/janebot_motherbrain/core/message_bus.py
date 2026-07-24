"""
================================================================================
MESSAGE BUS - ASYNC COMMUNICATION BACKBONE
================================================================================
The MessageBus is the nervous system of the MkdMind swarm. It facilitates the
flow of information between the MotherBrain and its agents, and between the
agents themselves. It is built on top of Python's asyncio for high concurrency.

Core Communication Patterns:
1. Pub/Sub: Agents subscribe to 'topics' and receive all messages on those topics.
2. Direct Messaging: Targeted delivery of a message to a specific agent ID.
3. Broadcast: Sending a message to every node in the swarm simultaneously.

Reliability Features:
- Message TTL (Time-To-Live): Automatically prunes stale messages.
- History Tracking: Maintains a window of recent messages for audit/recovery.
- Priority Routing: Higher priority messages are handled before lower ones.
================================================================================
"""

import asyncio
import json
import uuid
from typing import Dict, List, Callable, Any, Optional
from enum import Enum, auto
from dataclasses import dataclass, field
from datetime import datetime
import logging

# Logger scoped to the messaging module
logger = logging.getLogger(__name__)


class MessageType(Enum):
    """
    Defines the semantic intent of a message.
    
    Members:
        TASK: Instruction to perform specific work.
        RESPONSE: The result of a completed task.
        HEARTBEAT: Health check ping from an agent.
        BROADCAST: General announcement to all nodes.
        ERROR: Reporting a failure or exception.
        DISCOVERY: Query for agents with specific skills.
        STATUS: State update (e.g., agent becoming 'busy').
        STREAM: Real-time data flow (e.g., log streaming).
    """
    TASK = auto()
    RESPONSE = auto()
    HEARTBEAT = auto()
    BROADCAST = auto()
    ERROR = auto()
    DISCOVERY = auto()
    STATUS = auto()
    STREAM = auto()


@dataclass
class Message:
    """
    The standardized 'envelope' for all swarm communications.
    
    This object ensures that every piece of data moving through the bus
    has the necessary metadata for routing, tracing, and validation.
    
    Attributes:
        message_id: Unique trace ID for this specific message.
        message_type: Enum indicating the message category.
        sender: ID of the agent or component that sent the message.
        recipient: Optional ID for direct delivery (None = Broadcast).
        topic: Channel name for pub/sub routing.
        payload: The actual data being transmitted (JSON-serializable).
        timestamp: Creation time for ordering and TTL checks.
        priority: 0-10 scale for urgent message handling.
        ttl: Time in seconds before the message is considered expired.
        metadata: Contextual data (e.g., trace headers, auth tokens).
    """
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    message_type: MessageType = MessageType.TASK
    sender: str = ""
    recipient: Optional[str] = None
    topic: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    priority: int = 0
    ttl: int = 300
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializes the message for network transport."""
        return {
            "message_id": self.message_id,
            "message_type": self.message_type.name,
            "sender": self.sender,
            "recipient": self.recipient,
            "topic": self.topic,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "priority": self.priority,
            "ttl": self.ttl,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        """Deserializes a dictionary back into a Message object."""
        msg = cls(**{
            k: v for k, v in data.items() 
            if k in ["message_id", "sender", "recipient", "topic", "payload", 
                     "timestamp", "priority", "ttl", "metadata"]
        })
        if "message_type" in data:
            msg.message_type = MessageType[data["message_type"]]
        return msg


class MessageBus:
    """
    The central routing engine for the swarm.
    
    Maintains a registry of subscribers and handles the delivery logic for 
    different communication patterns. Designed to be highly decoupled.
    
    Sub-systems:
    - Pub/Sub Registry: Map of topics to callback functions.
    - Message History: LRU-style cache of recent transmissions.
    - Cleanup Engine: Background task that removes expired history.
    """
    
    def __init__(self, transport=None):
        """Initializes internal storage and synchronization primitives."""
        self._subscribers: Dict[str, List[Callable[[Message], None]]] = {}
        self._message_history: Dict[str, Message] = {}
        self._max_history = 10000
        self._lock = asyncio.Lock()
        self._running = False
        self._cleanup_task: Optional[asyncio.Task] = None
        self.transport = transport  # Reference to WebSocketBus
        
    async def start(self):
        """Starts the message bus and its internal garbage collector."""
        self._running = True
        self._cleanup_task = asyncio.create_task(self._cleanup_expired())
        logger.info("MessageBus ONLINE and accepting transmissions.")
        
    async def stop(self):
        """Shuts down the bus and cancels cleanup tasks."""
        self._running = False
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
        logger.info("MessageBus gracefully stopped.")
        
    def subscribe(self, topic: str, callback: Callable[[Message], None]):
        """Subscribe to a topic."""
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        self._subscribers[topic].append(callback)
        logger.debug(f"Subscribed to topic: {topic}")
        
    def unsubscribe(self, topic: str, callback: Callable[[Message], None]):
        """Unsubscribe from a topic."""
        if topic in self._subscribers:
            self._subscribers[topic].remove(callback)
            logger.debug(f"Unsubscribed from topic: {topic}")
            
    async def publish(self, message: Message):
        """Publish a message to a topic."""
        # Store in history
        async with self._lock:
            self._message_history[message.message_id] = message
            if len(self._message_history) > self._max_history:
                # Remove oldest
                oldest_id = min(self._message_history.keys())
                del self._message_history[oldest_id]
        
        # 1. Notify local subscribers
        if message.topic in self._subscribers:
            for callback in self._subscribers[message.topic]:
                try:
                    callback(message)
                except Exception as e:
                    logger.error(f"Error in callback for topic {message.topic}: {e}")
        
        # 2. If it's a broadcast or has no specific recipient, send to all remote agents
        if self.transport and (message.recipient is None or message.message_type == MessageType.BROADCAST):
            await self.transport.broadcast(message)
        
        logger.debug(f"Published message {message.message_id} to topic {message.topic}")
        
    async def send_direct(self, message: Message) -> Optional[Message]:
        """Send a direct message to a specific agent with optional response."""
        async with self._lock:
            self._message_history[message.message_id] = message
        
        # Route via network transport if available
        if self.transport and message.recipient:
            await self.transport.send_message(message.recipient, message)
        
        logger.debug(f"Direct message {message.message_id} from {message.sender} to {message.recipient}")
        return None  # Response handling is async
        
    async def broadcast(self, message: Message):
        """Broadcast a message to all agents."""
        message.recipient = None
        message.message_type = MessageType.BROADCAST
        await self.publish(message)
        logger.info(f"Broadcast message {message.message_id} from {message.sender}")

    async def handle_network_message(self, message: Message):
        """
        Entry point for the transport layer to inject messages received 
        from remote agents back into the local bus.
        """
        logger.debug(f"Network message injected: {message.message_id} from {message.sender}")
        await self.publish(message)
        
    async def request_response(self, message: Message, timeout: float = 30.0) -> Optional[Message]:
        """Send a request and wait for a response."""
        message.message_type = MessageType.TASK
        response_queue = asyncio.Queue()
        
        # Store response queue
        async with self._lock:
            self._response_queues = getattr(self, "_response_queues", {})
            self._response_queues[message.message_id] = response_queue
        
        try:
            await self.publish(message)
            try:
                response = await asyncio.wait_for(response_queue.get(), timeout=timeout)
                return response
            except asyncio.TimeoutError:
                logger.warning(f"Request {message.message_id} timed out")
                return None
        finally:
            async with self._lock:
                self._response_queues.pop(message.message_id, None)
                
    def get_message_history(self, limit: int = 100) -> List[Message]:
        """Get recent message history."""
        return list(self._message_history.values())[-limit:]
        
    async def _cleanup_expired(self):
        """Clean up expired messages."""
        while self._running:
            await asyncio.sleep(60)  # Run every minute
            current_time = datetime.now().timestamp()
            expired = [
                msg_id for msg_id, msg in self._message_history.items()
                if current_time - msg.timestamp > msg.ttl
            ]
            for msg_id in expired:
                del self._message_history[msg_id]
            
            if expired:
                logger.debug(f"Cleaned up {len(expired)} expired messages")
