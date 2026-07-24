import os
import requests

OLLAMA_URI = os.environ.get('OLLAMA_URI', 'http://127.0.0.1:11434')


def generate(prompt: str, model: str | None = None, timeout: int = 60) -> str:
    """Call local Ollama HTTP API and return generated text. Returns empty string on failure."""
    url = OLLAMA_URI.rstrip('/') + '/api/generate'
    payload = {"prompt": prompt, "stream": False}
    if model:
        payload['model'] = model
    try:
        resp = requests.post(url, json=payload, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        # Ollama returns {'response': '...'} in many setups; try common keys
        if isinstance(data, dict):
            if 'response' in data:
                return data['response']
            # some versions use 'generated' or other keys
            for k in ('generated_text', 'text', 'output'):
                if k in data:
                    return data[k]
            return str(data)
        return str(data)
    except Exception as e:
        return f"[Ollama error: {e}]"


def list_models(timeout: int = 5):
    try:
        resp = requests.get(OLLAMA_URI.rstrip('/') + '/api/tags', timeout=timeout)
        resp.raise_for_status()
        j = resp.json()
        return [m.get('name') for m in j.get('models', [])]
    except Exception:
        return []
