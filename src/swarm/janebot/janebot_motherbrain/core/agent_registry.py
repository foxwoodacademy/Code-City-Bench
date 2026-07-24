"""
================================================================================
AGENT REGISTRY - DYNAMIC DISCOVERY & LIFECYCLE MANAGEMENT
================================================================================
This module implements the 'Yellow Pages' of the swarm. It provides a centralized
directory where agents can register themselves, announce their capabilities,
and where the MotherBrain can discover the best-suited nodes for specific tasks.

Key Features:
- Real-time Registration: Agents join the swarm by submitting their metadata.
- Capability Indexing: Fast lookup of agents by what they can actually DO.
- Health Monitoring: Automated heartbeat checks to prune stale nodes.
- Load Tracking: Keeping tabs on which agents are busy and which are idle.
================================================================================
"""

import asyncio
import json
import uuid
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
import logging

# Logger scoped to the registry module
logger = logging.getLogger(__name__)


@dataclass
class AgentInfo:
    """
    Comprehensive descriptor for a single AI agent node.
    
    This object acts as the 'identity' of an agent within the swarm. It contains
    everything the MotherBrain needs to know to make routing decisions.
    
    Attributes:
        agent_id: Globally unique identifier (UUID string).
        name: Human-friendly name for logs and dashboards.
        version: Semantic version of the agent's software.
        description: Brief explanation of the agent's purpose.
        capabilities: List of skills (e.g., ['web_search', 'code_gen']).
        endpoints: Communication URLs (HTTP, WebSocket, gRPC).
        status: The current runtime state ('online', 'busy', 'error', etc.).
        last_heartbeat: Timestamp of the most recent health check.
        created_at: When this agent first joined the swarm.
        metadata: Arbitrary key-value pairs for extended configuration.
        tags: Searchable labels (e.g., ['gpu', 'low-latency']).
        priority: Relative importance for task allocation.
        max_concurrent: Maximum tasks this node can handle simultaneously.
        current_load: Number of tasks currently being processed.
    """
    agent_id: str
    name: str
    version: str = "1.0.0"
    description: str = ""
    capabilities: List[str] = field(default_factory=list)
    endpoints: Dict[str, str] = field(default_factory=dict)
    status: str = "offline"
    last_heartbeat: float = 0.0
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    priority: int = 5
    max_concurrent: int = 1
    current_load: int = 0
    
    def is_available(self) -> bool:
        """
        Determines if the agent is ready to accept a new task.
        
        Logic:
        - Must be 'online'.
        - Current workload must be less than its maximum capacity.
        """
        return self.status == "online" and self.current_load < self.max_concurrent
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializes the agent info for message bus transmission or persistence."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "capabilities": self.capabilities,
            "endpoints": self.endpoints,
            "status": self.status,
            "last_heartbeat": self.last_heartbeat,
            "created_at": self.created_at,
            "metadata": self.metadata,
            "tags": self.tags,
            "priority": self.priority,
            "max_concurrent": self.max_concurrent,
            "current_load": self.current_load
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentInfo":
        """Reconstructs an AgentInfo object from a dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


class AgentRegistry:
    """
    The central authority for agent metadata and health state.
    
    The Registry maintains a thread-safe map of all agents and optimized
    indices for quick discovery based on capabilities and tags.
    
    Lifecycle:
    1. start(): Launches a background monitor for heartbeats.
    2. register_agent(): Adds/updates an agent in the directory.
    3. get_agent(): Retrieves specific agent data.
    4. find_agents_by_capability(): Filters the swarm for specific skills.
    5. _monitor_heartbeats(): Periodically flags non-responsive nodes.
    """
    
    def __init__(self, message_bus=None):
        """
        Initializes the registry structures.
        
        Indices:
        - _agents: Main ID -> Object map.
        - _capability_index: Skill -> Set of Agent IDs for O(1) skill lookups.
        - _tag_index: Label -> Set of Agent IDs for O(1) tag lookups.
        """
        self._agents: Dict[str, AgentInfo] = {}
        self._capability_index: Dict[str, Set[str]] = {}
        self._tag_index: Dict[str, Set[str]] = {}
        self._message_bus = message_bus # Nervous system link
        self._lock = asyncio.Lock() # Ensures thread-safe registry modifications
        self._heartbeat_interval = 30.0
        self._heartbeat_timeout = 60.0
        self._running = False
        self._monitor_task: Optional[asyncio.Task] = None
        
    async def start(self):
        """
        Activates the registry monitoring loop.
        """
        self._running = True
        self._monitor_task = asyncio.create_task(self._monitor_heartbeats())
        logger.info("AgentRegistry initialized and monitoring heartbeats.")
        
    async def stop(self):
        """
        Deactivates monitoring and cleans up tasks.
        """
        self._running = False
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
        logger.info("AgentRegistry gracefully stopped.")
        
    async def register_agent(self, agent_info: AgentInfo) -> bool:
        """Register a new agent."""
        async with self._lock:
            if agent_info.agent_id in self._agents:
                logger.warning(f"Agent {agent_info.agent_id} already registered")
                return False
            
            self._agents[agent_info.agent_id] = agent_info
            
            # Update indexes
            for cap in agent_info.capabilities:
                if cap not in self._capability_index:
                    self._capability_index[cap] = set()
                self._capability_index[cap].add(agent_info.agent_id)
            
            for tag in agent_info.tags:
                if tag not in self._tag_index:
                    self._tag_index[tag] = set()
                self._tag_index[tag].add(agent_info.agent_id)
            
            logger.info(f"Registered agent: {agent_info.name} ({agent_info.agent_id})")
            
            # Notify via message bus if available
            if self._message_bus:
                from .message_bus import Message, MessageType
                msg = Message(
                    sender="registry",
                    topic="agent.registered",
                    message_type=MessageType.DISCOVERY,
                    payload={"agent_id": agent_info.agent_id, "agent_info": agent_info.to_dict()}
                )
                await self._message_bus.publish(msg)
            
            return True
            
    async def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent."""
        async with self._lock:
            if agent_id not in self._agents:
                return False
            
            agent_info = self._agents[agent_id]
            
            # Remove from indexes
            for cap in agent_info.capabilities:
                self._capability_index[cap].discard(agent_id)
            for tag in agent_info.tags:
                self._tag_index[tag].discard(agent_id)
            
            del self._agents[agent_id]
            logger.info(f"Unregistered agent: {agent_id}")
            return True

    async def handle_disconnect(self, agent_id: str):
        """
        Specifically handles an agent disconnecting from the network transport.
        Marks the agent as offline and notifies the swarm.
        """
        await self.update_agent_status(agent_id, "offline")
        logger.info(f"Agent {agent_id} disconnected from network transport")
        
        if self._message_bus:
            from .message_bus import Message, MessageType
            msg = Message(
                sender="registry",
                topic="agent.offline",
                message_type=MessageType.STATUS,
                payload={"agent_id": agent_id}
            )
            await self._message_bus.publish(msg)
            
    async def update_heartbeat(self, agent_id: str):
        """Update an agent's heartbeat."""
        async with self._lock:
            if agent_id in self._agents:
                self._agents[agent_id].last_heartbeat = datetime.now().timestamp()
                if self._agents[agent_id].status != "online":
                    self._agents[agent_id].status = "online"
                    logger.info(f"Agent {agent_id} is online")
                    
    async def update_agent_status(self, agent_id: str, status: str, load: int = None):
        """Update agent status and load."""
        async with self._lock:
            if agent_id in self._agents:
                self._agents[agent_id].status = status
                if load is not None:
                    self._agents[agent_id].current_load = load
                logger.debug(f"Agent {agent_id} status: {status}, load: {load}")
                
    async def get_agent(self, agent_id: str) -> Optional[AgentInfo]:
        """Get agent info by ID."""
        return self._agents.get(agent_id)
        
    async def list_agents(self, status_filter: Optional[str] = None) -> List[AgentInfo]:
        """List all registered agents with optional status filter."""
        agents = list(self._agents.values())
        if status_filter:
            agents = [a for a in agents if a.status == status_filter]
        return sorted(agents, key=lambda x: x.priority, reverse=True)
        
    async def find_by_capability(self, capability: str) -> List[AgentInfo]:
        """Find agents with a specific capability."""
        async with self._lock:
            agent_ids = self._capability_index.get(capability, set())
            return [self._agents[aid] for aid in agent_ids if aid in self._agents]
            
    async def find_by_tag(self, tag: str) -> List[AgentInfo]:
        """Find agents with a specific tag."""
        async with self._lock:
            agent_ids = self._tag_index.get(tag, set())
            return [self._agents[aid] for aid in agent_ids if aid in self._agents]
            
    async def find_available(self, capability: Optional[str] = None) -> List[AgentInfo]:
        """Find available agents, optionally filtered by capability."""
        agents = await self.list_agents(status_filter="online")
        if capability:
            agents = [a for a in agents if capability in a.capabilities]
        return [a for a in agents if a.is_available()]
        
    async def get_best_agent(self, capability: str) -> Optional[AgentInfo]:
        """Get the best available agent for a capability (highest priority, lowest load)."""
        agents = await self.find_available(capability)
        if not agents:
            return None
        return max(agents, key=lambda x: (x.priority, -x.current_load))
        
    async def _monitor_heartbeats(self):
        """Monitor agent heartbeats and mark offline agents."""
        while self._running:
            await asyncio.sleep(self._heartbeat_interval)
            current_time = datetime.now().timestamp()
            offline_agents = []
            
            async with self._lock:
                for agent_id, agent_info in self._agents.items():
                    if (current_time - agent_info.last_heartbeat > self._heartbeat_timeout and 
                        agent_info.status != "offline"):
                        agent_info.status = "offline"
                        offline_agents.append(agent_id)
                        logger.warning(f"Agent {agent_id} marked offline (no heartbeat)")
                
                # Notify via message bus
                if offline_agents and self._message_bus:
                    from .message_bus import Message, MessageType
                    msg = Message(
                        sender="registry",
                        topic="agent.offline",
                        message_type=MessageType.STATUS,
                        payload={"agent_ids": offline_agents}
                    )
                    await self._message_bus.publish(msg)
                    
    async def get_stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        async with self._lock:
            return {
                "total_agents": len(self._agents),
                "online_agents": sum(1 for a in self._agents.values() if a.status == "online"),
                "offline_agents": sum(1 for a in self._agents.values() if a.status == "offline"),
                "busy_agents": sum(1 for a in self._agents.values() if a.status == "busy"),
                "total_capabilities": len(self._capability_index),
                "capabilities": list(self._capability_index.keys()),
                "tags": list(self._tag_index.keys())
            }
