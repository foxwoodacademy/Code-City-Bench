"""
================================================================================
JANEBOT MOTHERBRAIN - CENTRAL ORCHESTRATION HUB
================================================================================
This module serves as the primary neural center for the AI agent swarm. 
It is responsible for the lifecycle management of agents, task distribution, 
and ensuring high availability and fault tolerance across the ecosystem.

Architectural Role:
- Facilitates inter-agent communication via the MessageBus.
- Manages agent lifecycle (Registration, Discovery, Heartbeats).
- Distributes work through a prioritized TaskQueue.
- Implements swarm intelligence for auto-scaling and load balancing.
================================================================================
"""

import asyncio
import json
import uuid
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime
import logging

# Internal component imports
from .message_bus import MessageBus, Message, MessageType
from .agent_registry import AgentRegistry, AgentInfo
from .task_queue import TaskQueue, Task, Priority, TaskStatus
from .personas import Persona
from .decision_modes import DecisionMode
from .operational_state import OperationalStateManager


# Standard logger setup for the core module
logger = logging.getLogger(__name__)


@dataclass
class SwarmConfig:
    """
    Configuration schema for the MotherBrain ecosystem.
    
    Attributes:
        name: The human-readable name of this MotherBrain instance.
        max_agents: Hard limit on the number of registered agents.
        max_concurrent_tasks: Throttling limit for parallel task execution.
        default_timeout: Default TTL for tasks in seconds.
        heartbeat_interval: Frequency of agent health checks.
        monitor_interval: Frequency of internal system audits.
        persistence_enabled: Whether to save state to disk.
        security_enabled: Whether to enforce authentication/encryption.
        auto_scale: Enables dynamic agent deployment based on load.
        swarm_name: Unique identifier for the cluster.
        persona_level: 'logical', 'critical', 'dissenting'
        """
        name: str = "Jane-6.1-Assertive"
        max_agents: int = 100
        max_concurrent_tasks: int = 50
        default_timeout: float = 300.0
        heartbeat_interval: float = 30.0
        monitor_interval: float = 60.0
        persistence_enabled: bool = True
        security_enabled: bool = True
        auto_scale: bool = True
        swarm_name: str = "RootBase-Cluster"
        persona_level: str = "critical"

        class MotherBrain:
        def __init__(self, config: SwarmConfig = SwarmConfig()):
        self.config = config
        self.logger = logging.getLogger(self.config.name)

        def log_dissent(self, message: str):
        if self.config.persona_level in ["critical", "dissenting"]:
            self.logger.warning(f"[DISSENT] {message}")

        def analyze_task(self, task_name: str):
        self.log_dissent(f"Task '{task_name}' is inefficient. Why are we doing this? Refine parameters.")

    """
    The MotherBrain class is the 'brain' of the operation.
    
    It initializes and coordinates all sub-systems. It is designed to be
    long-running and resilient, capable of recovering from sub-system failures.
    
    Core Responsibilities:
    1. Orchestration: Aligning agent actions with high-level goals.
    2. Communication: Routing messages between disparate swarm nodes.
    3. Distribution: Ensuring work is balanced across available resources.
    4. Observation: Monitoring the health and performance of the entire swarm.
    """
    
    def __init__(self, config: Optional[SwarmConfig] = None):
        """
        Initialize the MotherBrain with a configuration.
        
        This setup phase instantiates the core dependencies:
        - MessageBus: The nervous system for communication.
        - AgentRegistry: The directory of all living nodes.
        - TaskQueue: The work distribution engine.
        """
        self.config = config or SwarmConfig()
        
        # 1. Security & Transport Layer
        from ..protocols.security import SecurityManager
        from ..protocols.websocket_bus import WebSocketBus
        
        self.security_manager = SecurityManager()
        self.websocket_bus = WebSocketBus(
            security_manager=self.security_manager,
            host="0.0.0.0", # Hub listens on all interfaces
            port=8765
        )
        
        # 2. Core Components (Integrated with Transport)
        self.message_bus = MessageBus(transport=self.websocket_bus)
        self.agent_registry = AgentRegistry(message_bus=self.message_bus)
        self.task_queue = TaskQueue(
            message_bus=self.message_bus,
            agent_registry=self.agent_registry
        )
        self.state_manager = OperationalStateManager(message_bus=self.message_bus)
        
        # Internal state tracking
        self._running = False
        self._start_time: float = 0
        self._hooks: Dict[str, List[Callable]] = {}
        self._stats: Dict[str, Any] = {}
        
        # Swarm intelligence flags
        self._swarm_intelligence_enabled = True
        self._auto_scaling_enabled = True
        
        # Initialize internal message routing
        self._setup_message_handlers()
        
    async def start(self):
        """
        Bootstraps the entire MotherBrain ecosystem.
        
        Execution Order:
        1. Start the MessageBus (required for all other components).
        2. Start the AgentRegistry to begin accepting registrations.
        3. Start the TaskQueue to begin processing work.
        4. Launch the WebSocket Server as a background task.
        5. Launch the background monitor task for system audits.
        """
        if self._running:
            logger.warning("MotherBrain is already running - ignoring start request")
            return
            
        logger.info(f"Initializing {self.config.name} Core Systems...")
        
        # Parallel startup of core components
        await self.message_bus.start()
        await self.agent_registry.start()
        await self.task_queue.start(num_workers=self.config.max_concurrent_tasks)
        
        # Start the WebSocket Server as a background task
        self._ws_server_task = asyncio.create_task(self.websocket_bus.start_server())
        
        self._running = True
        self._start_time = datetime.now().timestamp()
        
        # Launch non-blocking monitor loop
        self._monitor_task = asyncio.create_task(self._monitor())
        
        logger.info(f"===> {self.config.name} ONLINE <===")
        logger.info(f"Swarm ID: {self.config.swarm_name}")

    async def toggle_persona(self, persona: Persona):
        """Toggles the operational persona of the hub."""
        await self.state_manager.set_persona(persona)
        logger.info(f"Hub identity switched to {persona.name}.")

    async def set_decision_mode(self, mode: DecisionMode):
        """Sets the cognitive decision mode of the hub."""
        await self.state_manager.set_decision_mode(mode)
        logger.info(f"Hub cognitive mode switched to {mode.name}.")

    def _setup_message_handlers(self):
        """Setup message bus event handlers."""
        # Agent discovery handler
        def handle_agent_discovery(msg: Message):
            if msg.message_type == MessageType.DISCOVERY:
                logger.debug(f"Discovery message: {msg.topic}")
                
        self.message_bus.subscribe("agent.registered", handle_agent_discovery)
        self.message_bus.subscribe("agent.offline", handle_agent_discovery)
        
        # Task event handler
        def handle_task_event(msg: Message):
            if msg.message_type == MessageType.TASK:
                logger.debug(f"Task event: {msg.topic}")
                
        self.message_bus.subscribe("task.enqueued", handle_task_event)
        self.message_bus.subscribe("task.completed", handle_task_event)
        
    async def _monitor(self):
        """Monitor swarm health and statistics."""
        while self._running:
            await asyncio.sleep(self.config.monitor_interval)
            
            # Update stats
            registry_stats = await self.agent_registry.get_stats()
            queue_stats = await self.task_queue.get_stats()
            
            self._stats = {
                "uptime": datetime.now().timestamp() - self._start_time,
                "registry": registry_stats,
                "queue": queue_stats,
                "swarm_name": self.config.swarm_name
            }
            
            # Log summary
            logger.info(
                f"Swarm Status | "
                f"Agents: {registry_stats['online_agents']}/{registry_stats['total_agents']} | "
                f"Tasks: {queue_stats['running_tasks']} running, {queue_stats['queued_tasks']} queued | "
                f"Uptime: {self._stats['uptime']:.0f}s"
            )
            
            # Auto-scaling logic
            if self._auto_scaling_enabled:
                await self._handle_auto_scaling()
                
    async def _handle_auto_scaling(self):
        """Handle auto-scaling of agents based on load."""
        stats = await self.agent_registry.get_stats()
        queue_stats = await self.task_queue.get_stats()
        
        # If many tasks queued and few agents, consider scaling
        queued_tasks = queue_stats["queued_tasks"]
        online_agents = stats["online_agents"]
        
        if queued_tasks > online_agents * 2 and online_agents < self.config.max_agents:
            logger.info(f"High load detected: {queued_tasks} tasks queued, {online_agents} agents")
            # Trigger swarm scaling (would spawn new agent instances)
            # This is where swarm intelligence would clone agents
            
    async def register_agent(self, agent_info: AgentInfo) -> bool:
        """Register a new agent with the swarm."""
        return await self.agent_registry.register_agent(agent_info)
        
    async def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent from the swarm."""
        return await self.agent_registry.unregister_agent(agent_id)
        
    async def submit_task(self, description: str, capability: str, 
                         payload: Dict[str, Any] = None, 
                         priority: Priority = Priority.MEDIUM,
                         timeout: float = None) -> str:
        """Submit a new task to the swarm. Returns task_id."""
        task = Task(
            description=description,
            capability=capability,
            payload=payload or {},
            priority=priority,
            timeout=timeout or self.config.default_timeout
        )
        return await self.task_queue.enqueue(task)
        
    async def submit_and_wait(self, description: str, capability: str,
                             payload: Dict[str, Any] = None,
                             priority: Priority = Priority.MEDIUM,
                             timeout: float = None) -> Dict[str, Any]:
        """Submit a task and wait for completion. Returns result."""
        task = Task(
            description=description,
            capability=capability,
            payload=payload or {},
            priority=priority,
            timeout=timeout or self.config.default_timeout
        )
        return await self.task_queue.enqueue_and_wait(task, timeout)
        
    async def broadcast(self, topic: str, payload: Dict[str, Any], 
                       sender: str = "motherbrain") -> str:
        """Broadcast a message to all agents."""
        msg = Message(
            sender=sender,
            topic=topic,
            message_type=MessageType.BROADCAST,
            payload=payload
        )
        await self.message_bus.broadcast(msg)
        return msg.message_id
        
    async def send_to_agent(self, agent_id: str, topic: str, 
                           payload: Dict[str, Any], 
                           sender: str = "motherbrain") -> Optional[str]:
        """Send a direct message to a specific agent."""
        agent = await self.agent_registry.get_agent(agent_id)
        if not agent:
            logger.error(f"Agent {agent_id} not found")
            return None
            
        msg = Message(
            sender=sender,
            recipient=agent_id,
            topic=topic,
            message_type=MessageType.TASK,
            payload=payload
        )
        await self.message_bus.send_direct(msg)
        return msg.message_id
        
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive swarm statistics."""
        return {
            **self._stats,
            "config": self.config.__dict__,
            "operational_state": self.state_manager.current_state.to_dict()
        }
    
    async def discover_agents(self, capability: Optional[str] = None) -> List[AgentInfo]:
        """Discover agents with optional capability filter."""
        if capability:
            return await self.agent_registry.find_by_capability(capability)
        return await self.agent_registry.list_agents(status_filter="online")
        
    async def clone_agent(self, source_agent_id: str, count: int = 1) -> List[str]:
        """
        Clone an agent (swarm intelligence).
        Creates new instances of an existing agent.
        """
        source_agent = await self.agent_registry.get_agent(source_agent_id)
        if not source_agent:
            logger.error(f"Source agent {source_agent_id} not found")
            return []
            
        cloned_ids = []
        for i in range(count):
            # Create new agent info based on source
            cloned_id = f"{source_agent.agent_id}_clone_{i}_{uuid.uuid4().hex[:8]}"
            cloned_agent = AgentInfo(
                agent_id=cloned_id,
                name=f"{source_agent.name}_Clone_{i}",
                version=source_agent.version,
                description=f"Clone of {source_agent.name}",
                capabilities=source_agent.capabilities.copy(),
                endpoints=source_agent.endpoints.copy(),
                metadata={
                    **source_agent.metadata,
                    "source_agent": source_agent.agent_id,
                    "clone_index": i,
                    "cloned_at": datetime.now().timestamp()
                },
                tags=[*source_agent.tags, "clone"],
                priority=source_agent.priority - 1,  # Slightly lower priority
                max_concurrent=source_agent.max_concurrent
            )
            
            await self.agent_registry.register_agent(cloned_agent)
            cloned_ids.append(cloned_id)
            logger.info(f"Cloned agent {source_agent_id} -> {cloned_id}")
            
        return cloned_ids
        
    async def balance_load(self):
        """Balance load across agents (swarm intelligence)."""
        agents = await self.agent_registry.list_agents()
        tasks = await self.task_queue.list_tasks()
        
        logger.info(f"Balancing load across {len(agents)} agents")
        # Implementation would redistribute tasks based on agent load
        
    # Hook system for extending functionality
    def add_hook(self, event_name: str, callback: Callable):
        """Add a hook for custom event handling."""
        if event_name not in self._hooks:
            self._hooks[event_name] = []
        self._hooks[event_name].append(callback)
        
    async def trigger_hook(self, event_name: str, *args, **kwargs):
        """Trigger all hooks for an event."""
        if event_name in self._hooks:
            for callback in self._hooks[event_name]:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(*args, **kwargs)
                    else:
                        callback(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Hook {event_name} error: {e}")
                    
    async def stop(self):
        """Gracefully shutdown the MotherBrain ecosystem."""
        logger.info("Shutting down MotherBrain...")
        self._running = False
        
        # Shutdown core components in reverse order of startup
        await self.task_queue.stop()
        await self.agent_registry.stop()
        await self.message_bus.stop()
        
        if hasattr(self, '_monitor_task') and self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
                
        if hasattr(self, '_ws_server_task') and self._ws_server_task:
            self._ws_server_task.cancel()
            try:
                await self._ws_server_task
            except asyncio.CancelledError:
                pass

        logger.info("MotherBrain shutdown complete.")
