# Agent Manager
# Responsible for agent lifecycle, registry, and swarm coordination.

from typing import Dict
from .base_agent import BaseAgent

class AgentManager:
    """
    Central orchestrator for agent lifecycle management.
    Handles agent registration, lookups, and provides basic discovery within the swarm.
    """
    def __init__(self):
        self._registry: Dict[str, BaseAgent] = {}

    def register_agent(self, agent: BaseAgent):
        """Register an agent instance into the swarm registry."""
        self._registry[agent.name] = agent
        print(f"Agent '{agent.name}' registered.")

    def get_agent(self, name: str) -> BaseAgent:
        """Retrieve an agent instance by name."""
        return self._registry.get(name)

    def list_agents(self):
        """List all currently registered agents."""
        return list(self._registry.keys())
