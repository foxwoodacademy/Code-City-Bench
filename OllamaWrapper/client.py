"""
OllamaWrapper: Local Reasoning Engine.
Provides a unified, hardened interface for the swarm to query local Ollama models.
"""

import aiohttp
import logging
import asyncio
from typing import Dict, Any, Optional, List
from path_resolver import resolver

# Setup logging for the reasoning engine
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OllamaWrapper")

class OllamaWrapper:
    """
    Standardized connector for the local Ollama reasoning engine.
    Implements retry logic, model profiling, and async context management.
    """
    def __init__(self, base_url: str = "http://localhost:11434", timeout: int = 60):
        self.base_url = base_url
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        # Model Profiles: mappings for different agentic needs
        self.profiles = {
            "reasoning": "llama3",
            "creative": "mistral",
            "fast": "phi3",
            "deep": "deepseek-coder"
        }

    async def query(self, prompt: str, profile: str = "reasoning", context: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Sends a prompt to the local Ollama instance.
        
        Args:
            prompt: The primary query.
            profile: Use 'reasoning', 'creative', 'fast', or 'deep'.
            context: Optional list of previous messages for conversational state.
        """
        model = self.profiles.get(profile, self.profiles["reasoning"])
        
        # Format payload for /api/chat (allows for context/messages)
        messages = context or []
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.2 if profile == "reasoning" else 0.7,
                "num_ctx": 4096
            }
        }

        max_retries = 3
        for attempt in range(max_retries):
            try:
                async with aiohttp.ClientSession(timeout=self.timeout) as session:
                    async with session.post(f"{self.base_url}/api/chat", json=payload) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            return data.get("message", {}).get("content", "")
                        else:
                            logger.warning(f"Ollama API returned status {resp.status} (Attempt {attempt+1}/{max_retries})")
            except Exception as e:
                logger.error(f"Ollama reasoning connection failure: {e} (Attempt {attempt+1}/{max_retries})")
            
            # Exponential backoff before retry
            await asyncio.sleep(2 ** attempt)

        return "Analysis engine unavailable after multiple attempts."

    def update_profile(self, profile_name: str, model_name: str):
        """Dynamically update model profiles based on current local availability."""
        self.profiles[profile_name] = model_name
        logger.info(f"Profile '{profile_name}' updated to model '{model_name}'.")
