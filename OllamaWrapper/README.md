# OllamaWrapper: Production-Grade Local Reasoning Engine

The OllamaWrapper provides a hardened, unified interface for the RootBase swarm to query local LLMs via Ollama. It transforms a simple API connector into a robust reasoning engine capable of supporting complex agentic workflows.

## 🚀 Professional Features
- **Model Profiling**: Pre-configured profiles for different task types:
  - `reasoning`: Low temperature, high precision (e.g., Llama3).
  - `creative`: Higher temperature for divergent thinking (e.g., Mistral).
  - `fast`: Lightweight models for rapid tasks (e.g., Phi3).
  - `deep`: Specialized models for code and complex logic (e.g., DeepSeek-Coder).
- **Resilient Connectivity**: Implements exponential backoff and retry logic to handle local engine load and transient failures.
- **Stateful Context**: Supports full message history via the `/api/chat` endpoint, enabling multi-turn reasoning.
- **Adaptive Timeout**: Configurable asynchronous timeouts to prevent agent hanging.

## 🛠 Integration
Inject this into any agent requiring local reasoning:

```python
from OllamaWrapper.client import OllamaWrapper

# Initialize the engine
brain = OllamaWrapper()

# Query with a specific profile for high-precision reasoning
insight = await brain.query(
    prompt="Analyze the structural integrity of this module.",
    profile="reasoning",
    context=[{"role": "system", "content": "You are a senior security auditor."}]
)
```

## ⚙️ Configuration
The engine is integrated with the `PathResolver` to ensure consistent operation across the RootBase ecosystem.
