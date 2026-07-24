"""
BrainAdapter - Interface to switch between local (Ollama) and cloud LLM providers.
Provides a unified semantic inference API for NatCommand.
"""

import logging
from abc import ABC, abstractmethod
import requests # Placeholder for API calls

logger = logging.getLogger("NatCommand.Brain")

class BrainProvider(ABC):
    @abstractmethod
    def infer_intent(self, text: str) -> str:
        pass

class OllamaProvider(BrainProvider):
    def __init__(self, model="gemma2"):
        self.model = model
    
    def infer_intent(self, text: str) -> str:
        # Calls local Ollama API
        logger.info(f"🧠 Querying local {self.model} for intent: '{text}'")
        return "checkpoint" # Simulated response

class CloudProvider(BrainProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def infer_intent(self, text: str) -> str:
        # Calls external API (Gemini Cloud, etc)
        logger.info(f"☁️ Querying cloud LLM for complex intent: '{text}'")
        return "checkpoint"

class BrainAdapter:
    def __init__(self, use_cloud=False):
        self.provider = CloudProvider(api_key="sk-...") if use_cloud else OllamaProvider()

    def get_intent(self, text: str) -> str:
        return self.provider.infer_intent(text)
