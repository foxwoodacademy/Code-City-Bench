"""
Base Agent - Standard interface for all agents in the swarm.
Every agent must implement this interface for compatibility.
"""

import asyncio
import json
import uuid
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
import logging

from janebot_motherbrain.core.message_bus import Message, MessageType
from janebot_motherbrain.core.agent_registry import AgentInfo

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Agent runtime status."""
    STOPPED = auto()
    STARTING = auto()
    IDLE = auto()
    BUSY = auto()
    ERROR = auto()
    SHUTTING_DOWN = auto()


class AgentType(Enum):
    """Agent type classification."""
    LLM = "llm"              # Large Language Model
    TOOL = "tool"            # Specialized tool/function
    ORCHESTRATOR = "orchestrator"  # Coordinates other agents
    SCOUT = "scout"          # Information gathering
    CLONER = "cloner"        # Can spawn copies
    SCRAPER = "scraper"      # Web/data scraping
    RESEARCH = "research"    # R&D, physics, etc.
    SAAS = "saas"           # SaaS service
    DEFENSE = "defense"      # Defense contracting
    MARKETING = "marketing"  # Marketing/branding
    SOCIAL = "social"        # Social influence
    ANALYTICS = "analytics"  # Data analysis
    STORAGE = "storage"      # Memory/persistence
    SECURITY = "security"    # Security monitoring
    DEPLOYMENT = "deployment"  # Deployment/CI/CD


@dataclass
class AgentCapability:
    """Defines an agent's capability."""
    name: str
    description: str = ""
    input_schema: Dict[str, Any] = field(default_factory=dict)
    output_schema: Dict[str, Any] = field(default_factory=dict)
    examples: List[Dict[str, Any]] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "examples": self.examples,
            "tags": self.tags
        }


@dataclass
class AgentResult:
    """Result from an agent operation."""
    success: bool
    output: Any = None
    error: Optional[str] = None
    task_id: Optional[str] = None
    agent_id: Optional[str] = None
    execution_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "execution_time": self.execution_time,
            "metadata": self.metadata
        }


class BaseAgent(ABC):
    """
    Base class for all agents in the MotherBrain swarm.
    
    Every agent must:
    1. Have a unique agent_id
    2. Register with the MotherBrain on startup
    3. Respond to messages on the message bus
    4. Send heartbeats
    5. Handle tasks assigned to it
    
    Agents can:
    - Communicate with other agents via message bus
    - Submit tasks to the task queue
    - Clone themselves (if ClonerAgent)
    - Discover other agents
    """
    
    def __init__(self, 
                 name: str, 
                 agent_type: AgentType = AgentType.TOOL,
                 description: str = "",
                 version: str = "1.0.0",
                 capabilities: List[str] = None,
                 tags: List[str] = None,
                 max_concurrent: int = 1,
                 priority: int = 5):
        
        self.agent_id = f"{name.lower().replace(' ', '_')}_{uuid.uuid4().hex[:8]}"
        self.name = name
        self.agent_type = agent_type
        self.description = description
        self.version = version
        self.capabilities = capabilities or []
        self.tags = tags or [agent_type.value]
        self.max_concurrent = max_concurrent
        self.priority = priority
        
        # Runtime state
        self.status = AgentStatus.STOPPED
        self.current_tasks: Dict[str, asyncio.Task] = {}
        self.current_load = 0
        self.message_bus = None
        self.motherbrain = None
        self.agent_registry = None
        
        # Configuration
        self._heartbeat_interval = 15.0  # seconds
        self._heartbeat_task: Optional[asyncio.Task] = None
        self._message_handler_task: Optional[asyncio.Task] = None
        self.operational_state: Dict[str, Any] = {}
        
        # Metrics
        self.metrics = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "started_at": None,
            "last_activity": None
        }
        
    @property
    def agent_info(self) -> AgentInfo:
        """Get AgentInfo for registration."""
        return AgentInfo(
            agent_id=self.agent_id,
            name=self.name,
            version=self.version,
            description=self.description,
            capabilities=self.capabilities,
            tags=self.tags,
            priority=self.priority,
            max_concurrent=self.max_concurrent,
            metadata={
                "agent_type": self.agent_type.value,
                "status": self.status.name
            }
        )
    
    def set_motherbrain(self, motherbrain):
        """Connect to MotherBrain."""
        self.motherbrain = motherbrain
        self.message_bus = motherbrain.message_bus
        self.agent_registry = motherbrain.agent_registry
        
    async def start(self):
        """Start the agent."""
        if self.status != AgentStatus.STOPPED:
            logger.warning(f"Agent {self.name} is already running")
            return
            
        logger.info(f"Starting agent: {self.name} ({self.agent_id})")
        
        self.status = AgentStatus.STARTING
        self.metrics["started_at"] = datetime.now().timestamp()
        
        # Initialize agent-specific components
        await self._initialize()
        
        # Register with MotherBrain
        if self.motherbrain:
            await self.motherbrain.agent_registry.register_agent(self.agent_info)
            await self.motherbrain.agent_registry.update_heartbeat(self.agent_id)
        
        # Start heartbeat
        self._heartbeat_task = asyncio.create_task(self._send_heartbeats())
        
        # Start message handler
        self._message_handler_task = asyncio.create_task(self._handle_messages())
        
        self.status = AgentStatus.IDLE
        logger.info(f"Agent {self.name} started")
        
    async def stop(self):
        """Stop the agent."""
        if self.status == AgentStatus.STOPPED:
            return
            
        logger.info(f"Stopping agent: {self.name}")
        self.status = AgentStatus.SHUTTING_DOWN
        
        # Cancel all running tasks
        for task_id, task in self.current_tasks.items():
            task.cancel()
        
        # Stop heartbeat
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass
                
        # Stop message handler
        if self._message_handler_task:
            self._message_handler_task.cancel()
            try:
                await self._message_handler_task
            except asyncio.CancelledError:
                pass
        
        # Unregister from MotherBrain
        if self.motherbrain:
            await self.motherbrain.agent_registry.unregister_agent(self.agent_id)
        
        # Cleanup
        await self._cleanup()
        
        self.status = AgentStatus.STOPPED
        logger.info(f"Agent {self.name} stopped")
        
    async def _initialize(self):
        """Initialize agent-specific components. Override in subclasses."""
        pass
        
    async def _cleanup(self):
        """Cleanup agent resources. Override in subclasses."""
        pass
        
    async def _send_heartbeats(self):
        """Send periodic heartbeats."""
        while self.status != AgentStatus.STOPPED:
            try:
                if self.agent_registry:
                    await self.agent_registry.update_heartbeat(self.agent_id)
                await asyncio.sleep(self._heartbeat_interval)
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
                await asyncio.sleep(5)
                
    async def _handle_messages(self):
        """Handle incoming messages from the message bus."""
        if not self.message_bus:
            return
            
        # Subscribe to direct messages
        def handle_message(msg: Message):
            if msg.recipient == self.agent_id or msg.recipient is None:
                asyncio.create_task(self._process_message(msg))
                
        self.message_bus.subscribe(f"agent.{self.agent_id}", handle_message)
        self.message_bus.subscribe(f"task.execute.{self.agent_id}", handle_message)
        
        # Also subscribe to broadcast messages
        self.message_bus.subscribe("broadcast", handle_message)
        self.message_bus.subscribe("system.operational_state_change", handle_message)
        
        # Keep running
        while self.status != AgentStatus.STOPPED:
            await asyncio.sleep(1)
            
    async def _handle_state_change(self, msg: Message):
        """React to operational state changes."""
        self.operational_state = msg.payload
        logger.info(f"Agent {self.name} reacting to state change: {self.operational_state.get('persona_name')}")
        await self.on_state_change(self.operational_state)

    async def on_state_change(self, new_state: Dict[str, Any]):
        """Agent-specific reaction logic. Override in subclasses."""
        pass
            
    async def _process_message(self, msg: Message):
        """Process an incoming message."""
        self.metrics["messages_received"] += 1
        self.metrics["last_activity"] = datetime.now().timestamp()
        
        try:
            if msg.message_type == MessageType.TASK:
                # Handle task execution
                task_id = msg.payload.get("task_id", msg.message_id)
                capability = msg.payload.get("capability", "")
                
                if capability in self.capabilities:
                    await self._execute_task(msg)
                else:
                    logger.warning(f"Agent {self.name} does not have capability: {capability}")
                    
            elif msg.topic == "system.operational_state_change":
                await self._handle_state_change(msg)
                
            elif msg.message_type == MessageType.BROADCAST:
                await self._handle_broadcast(msg)
                
            elif msg.message_type == MessageType.DISCOVERY:
                await self._handle_discovery(msg)
                
            else:
                await self._handle_custom_message(msg)
                
        except Exception as e:
            logger.error(f"Error processing message {msg.message_id}: {e}")
            
    async def _execute_task(self, msg: Message):
        """Execute a task assigned to this agent."""
        task_id = msg.payload.get("task_id", msg.message_id)
        payload = msg.payload.get("payload", {})
        capability = msg.payload.get("capability", "")
        
        logger.info(f"Agent {self.name} executing task {task_id}: {capability}")
        
        # Update status
        if self.motherbrain:
            await self.motherbrain.agent_registry.update_agent_status(
                self.agent_id, "busy", self.current_load + 1
            )
        self.current_load += 1
        
        try:
            # Execute the task
            start_time = datetime.now().timestamp()
            result = await self.execute(capability, payload)
            execution_time = datetime.now().timestamp() - start_time
            
            # Send response
            response_msg = Message(
                message_id=task_id,
                sender=self.agent_id,
                recipient=msg.sender,
                topic=f"task.completed.{task_id}",
                message_type=MessageType.RESPONSE,
                payload={
                    "task_id": task_id,
                    "status": "completed",
                    "result": result,
                    "execution_time": execution_time,
                    "agent_id": self.agent_id
                }
            )
            await self.message_bus.publish(response_msg)
            
            self.metrics["tasks_completed"] += 1
            logger.info(f"Agent {self.name} completed task {task_id}")
            
        except Exception as e:
            error_msg = Message(
                message_id=task_id,
                sender=self.agent_id,
                recipient=msg.sender,
                topic=f"task.failed.{task_id}",
                message_type=MessageType.ERROR,
                payload={
                    "task_id": task_id,
                    "status": "failed",
                    "error": str(e),
                    "agent_id": self.agent_id
                }
            )
            await self.message_bus.publish(error_msg)
            
            self.metrics["tasks_failed"] += 1
            logger.error(f"Agent {self.name} failed task {task_id}: {e}")
            
        finally:
            self.current_load -= 1
            if self.motherbrain:
                await self.motherbrain.agent_registry.update_agent_status(
                    self.agent_id, "online", self.current_load
                )
                
    async def _handle_broadcast(self, msg: Message):
        """Handle broadcast messages. Override in subclasses."""
        pass
        
    async def _handle_discovery(self, msg: Message):
        """Handle discovery messages. Override in subclasses."""
        pass
        
    async def _handle_custom_message(self, msg: Message):
        """Handle custom message types. Override in subclasses."""
        pass
        
    @abstractmethod
    async def execute(self, capability: str, payload: Dict[str, Any]) -> Any:
        """
        Execute a capability.
        
        Args:
            capability: The capability to execute
            payload: Input data for the capability
            
        Returns:
            Result of the execution
        """
        pass
        
    def get_metrics(self) -> Dict[str, Any]:
        """Get agent metrics."""
        return {
            **self.metrics,
            "agent_id": self.agent_id,
            "name": self.name,
            "status": self.status.name,
            "current_load": self.current_load,
            "capabilities": self.capabilities
        }
    
    async def discover_agents(self, capability: Optional[str] = None) -> List[Any]:
        """Discover other agents with optional capability filter."""
        if self.motherbrain:
            return await self.motherbrain.discover_agents(capability)
        return []
        
    async def send_message(self, recipient: str, topic: str, 
                           payload: Dict[str, Any], 
                           message_type: MessageType = MessageType.TASK) -> str:
        """Send a message to another agent."""
        if not self.message_bus:
            raise RuntimeError("No message bus connected")
            
        msg = Message(
            sender=self.agent_id,
            recipient=recipient,
            topic=topic,
            message_type=message_type,
            payload=payload
        )
        await self.message_bus.publish(msg)
        self.metrics["messages_sent"] += 1
        return msg.message_id
        
    async def broadcast(self, topic: str, payload: Dict[str, Any]) -> str:
        """Broadcast a message to all agents."""
        if not self.message_bus:
            raise RuntimeError("No message bus connected")
            
        msg = Message(
            sender=self.agent_id,
            topic=topic,
            message_type=MessageType.BROADCAST,
            payload=payload
        )
        await self.message_bus.broadcast(msg)
        self.metrics["messages_sent"] += 1
        return msg.message_id
        
    async def submit_task(self, description: str, capability: str,
                         payload: Dict[str, Any] = None,
                         priority: int = 5) -> str:
        """Submit a task to the task queue."""
        if not self.motherbrain:
            raise RuntimeError("No MotherBrain connected")
            
        from janebot_motherbrain.core.task_queue import Priority as TaskPriority
        
        priority_map = {
            10: TaskPriority.CRITICAL,
            8: TaskPriority.HIGH,
            5: TaskPriority.MEDIUM,
            3: TaskPriority.LOW,
            1: TaskPriority.BACKGROUND
        }
        
        task_priority = priority_map.get(priority, TaskPriority.MEDIUM)
        return await self.motherbrain.submit_task(description, capability, payload, task_priority)
        
    # Utility methods
    async def wait_for_agents(self, capability: str, min_count: int = 1, timeout: float = 60.0):
        """Wait for agents with a specific capability to be available."""
        start_time = datetime.now().timestamp()
        
        while datetime.now().timestamp() - start_time < timeout:
            agents = await self.discover_agents(capability)
            available = [a for a in agents if a.is_available()]
            
            if len(available) >= min_count:
                return available
            
            await asyncio.sleep(1)
            
        return []
