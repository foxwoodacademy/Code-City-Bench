# Core Agent Engine

from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """
    Abstract base class for all agentic engines.
    Ensures consistent interface for execution and interaction.
    """
    def __init__(self, name: str, persona: dict):
        self.name = name
        self.persona = persona

    @abstractmethod
    def execute(self, task: str):
        """Execute the assigned task based on persona definition."""
        pass
