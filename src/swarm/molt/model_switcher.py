import psutil
import json
import requests

def ask_ollama(prompt: str, model: str, host: str = "http://127.0.0.1:11434"):
    """Query Ollama with a specific model."""
    try:
        resp = requests.post(
            f"{host}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.7}
            },
            timeout=600
        )
        resp.raise_for_status()
        return resp.json().get("response", "").strip(), True
    except Exception as e:
        return f"Error: {e}", False

class ModelSwitcher:
    def __init__(self, primary="qwen2.5:7b", fallback="qwen2.5-coder:1.5b"):
        self.primary = primary
        self.fallback = fallback

    def get_system_load(self):
        """Check available memory."""
        mem = psutil.virtual_memory()
        return mem.available / (1024 ** 3)  # GB available

    def get_optimal_model(self):
        """Returns optimal model based on available RAM (threshold 4GB)."""
        if self.get_system_load() > 4.0:
            return self.primary
        return self.fallback

# --- Workflow ---
# switcher = ModelSwitcher()
# model = switcher.select_model()
# # If model == fallback: use to parse/draft
# # If model == primary: use to analyze
