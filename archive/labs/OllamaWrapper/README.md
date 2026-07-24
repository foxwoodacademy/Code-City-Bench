# OllamaWrapper README

This module provides the core reasoning capability for all swarm agents.

## Features
- **Standardized API**: Unified `query` method for all agents.
- **Local-First**: Connects to the local Ollama instance running on your tablet/device.
- **Error Handling**: Graceful fallback if the engine is down.

## Integration
Inject this into any `BaseAgent` subclass requiring complex reasoning:
```python
from OllamaWrapper.client import OllamaWrapper
self.brain = OllamaWrapper()
```
