"""
Agent implementations and base classes for the MotherBrain swarm.

Agent Types:
- BaseAgent: Standard agent interface
- LLMAgent: Large Language Model agents (Hermes, Mistral, etc.)
- ToolAgent: Agents with specialized tools
- OrchestratorAgent: Agents that coordinate other agents
- ScoutAgent: Information gathering agents
- ClonerAgent: Agents that can spawn copies of themselves
- ScraperAgent: Web/data scraping agents
- ResearchAgent: Physics and R&D agents
- SaaSAgent: SaaS service agents
- DefenseAgent: Defense/contracting agents
"""

from .base_agent import BaseAgent, AgentStatus
from .llm_agent import LLMAgent
from .tool_agent import ToolAgent
from .orchestrator_agent import OrchestratorAgent

__all__ = ["BaseAgent", "AgentStatus", "LLMAgent", "ToolAgent", "OrchestratorAgent"]
