"""
OllamaWrapper: Local Reasoning Engine.
Provides a unified interface for the swarm to query local Ollama models.
"""

import aiohttp
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class OllamaWrapper:
    """
    Standardized connector for the local Ollama reasoning engine.
    Usage:
        brain = OllamaWrapper()
        insight = await brain.query("Analyze this market trend...")
    """
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url

    async def query(self, prompt: str, model: str = "llama3") -> str:
        """Sends a prompt to the local Ollama instance."""
        async with aiohttp.ClientSession() as session:
            payload = {"model": model, "prompt": prompt, "stream": False}
            try:
                async with session.post(f"{self.base_url}/api/generate", json=payload) as resp:
                    data = await resp.json()
                    return data.get("response", "")
            except Exception as e:
                logger.error(f"Ollama reasoning failed: {e}")
                return "Analysis engine unavailable."
