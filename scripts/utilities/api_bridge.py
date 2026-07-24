#!/usr/bin/env python3
"""
CodeMentor API Bridge
Model-agnostic layer. Routes to whatever's available:
- Ollama (local, free tier)
- Claude API (paid tier, best quality)
- Kimi/OpenRouter (alternative paid)

Priority: Claude > Ollama > fallback error

Set environment variables to configure:
  CODEMENTOR_BACKEND=claude|ollama|kimi   (force a backend)
  ANTHROPIC_API_KEY=sk-ant-...            (enables Claude)
  OPENROUTER_API_KEY=...                  (enables Kimi via OpenRouter)
  OLLAMA_HOST=http://localhost:11434      (default)
  OLLAMA_MODEL=qwen2.5:1.5b              (default)
"""

import os
import json
import requests
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class MentorResponse:
    """Structured response from any backend."""
    content: str
    backend: str
    model: str
    success: bool
    error: Optional[str] = None
    tokens_used: Optional[int] = None


class APIBridge:
    """
    Single interface to all AI backends.
    CodeMentor core never needs to know which model is running.
    """

    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")
    ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY", "")
    FORCED_BACKEND = os.getenv("CODEMENTOR_BACKEND", "")

    # Claude model to use
    CLAUDE_MODEL = "claude-sonnet-4-20250514"

    def __init__(self):
        self.active_backend = self._detect_backend()

    def _detect_backend(self) -> str:
        """Auto-detect best available backend."""
        if self.FORCED_BACKEND:
            return self.FORCED_BACKEND

        # Claude first - best quality
        if self.ANTHROPIC_KEY:
            return "claude"

        # OpenRouter / Kimi second
        if self.OPENROUTER_KEY:
            return "openrouter"

        # Ollama last - always available locally
        return "ollama"

    def generate(self, prompt: str, system: Optional[str] = None,
                 max_tokens: int = 1500) -> MentorResponse:
        """
        Generate a response. Automatically falls back if primary fails.
        """
        backends = self._get_fallback_chain()

        for backend in backends:
            try:
                if backend == "claude":
                    return self._call_claude(prompt, system, max_tokens)
                elif backend == "openrouter":
                    return self._call_openrouter(prompt, system, max_tokens)
                elif backend == "ollama":
                    return self._call_ollama(prompt, system, max_tokens)
            except Exception as e:
                print(f"[APIBridge] {backend} failed: {e}, trying next...")
                continue

        return MentorResponse(
            content="",
            backend="none",
            model="none",
            success=False,
            error="All backends failed. Check Ollama is running: ollama serve"
        )

    def _get_fallback_chain(self):
        """Return backends in priority order starting from active."""
        all_backends = ["claude", "openrouter", "ollama"]
        chain = [self.active_backend]
        for b in all_backends:
            if b not in chain:
                chain.append(b)
        return chain

    def _call_claude(self, prompt: str, system: Optional[str],
                     max_tokens: int) -> MentorResponse:
        """Call Anthropic Claude API."""
        if not self.ANTHROPIC_KEY:
            raise ValueError("No ANTHROPIC_API_KEY set")

        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.ANTHROPIC_KEY,
            "anthropic-version": "2023-06-01"
        }

        body: Dict[str, Any] = {
            "model": self.CLAUDE_MODEL,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}]
        }
        if system:
            body["system"] = system

        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=body,
            timeout=60
        )
        resp.raise_for_status()
        data = resp.json()

        content = data["content"][0]["text"]
        tokens = data.get("usage", {}).get("output_tokens")

        return MentorResponse(
            content=content,
            backend="claude",
            model=self.CLAUDE_MODEL,
            success=True,
            tokens_used=tokens
        )

    def _call_openrouter(self, prompt: str, system: Optional[str],
                         max_tokens: int) -> MentorResponse:
        """Call OpenRouter (Kimi or other models)."""
        if not self.OPENROUTER_KEY:
            raise ValueError("No OPENROUTER_API_KEY set")

        model = os.getenv("OPENROUTER_MODEL", "qwen/qwen3-8b:free")

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.OPENROUTER_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens
            },
            timeout=60
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]

        return MentorResponse(
            content=content,
            backend="openrouter",
            model=model,
            success=True
        )

    def _call_ollama(self, prompt: str, system: Optional[str],
                     max_tokens: int) -> MentorResponse:
        """Call local Ollama instance."""
        full_prompt = f"{system}\n\n{prompt}" if system else prompt

        resp = requests.post(
            f"{self.OLLAMA_HOST}/api/generate",
            json={
                "model": self.OLLAMA_MODEL,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": max_tokens
                }
            },
            timeout=300
        )
        resp.raise_for_status()
        content = resp.json().get("response", "").strip()

        return MentorResponse(
            content=content,
            backend="ollama",
            model=self.OLLAMA_MODEL,
            success=True
        )

    def health_check(self) -> Dict[str, bool]:
        """Check which backends are currently available."""
        status = {}

        # Claude
        status["claude"] = bool(self.ANTHROPIC_KEY)

        # OpenRouter
        status["openrouter"] = bool(self.OPENROUTER_KEY)

        # Ollama - actually ping it
        try:
            resp = requests.get(
                f"{self.OLLAMA_HOST}/api/tags", timeout=3
            )
            status["ollama"] = resp.status_code == 200
        except Exception:
            status["ollama"] = False

        status["active_backend"] = self.active_backend
        return status


# Singleton for import
bridge = APIBridge()


if __name__ == "__main__":
    print("CodeMentor API Bridge - Health Check")
    print("=" * 40)
    health = bridge.health_check()
    for k, v in health.items():
        icon = "✅" if v else "❌"
        if k == "active_backend":
            print(f"  Active backend: {v}")
        else:
            print(f"  {icon} {k}")

    print()
    print("Testing active backend with a simple prompt...")
    result = bridge.generate(
        prompt="Say 'CodeMentor bridge is working' and nothing else.",
        max_tokens=20
    )
    if result.success:
        print(f"✅ Response: {result.content}")
        print(f"   Backend: {result.backend} / {result.model}")
    else:
        print(f"❌ Failed: {result.error}")
