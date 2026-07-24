"""Thoth client stub
Best-effort thin client to call local Ollama for persona responses.
Falls back to a helpful error string if Ollama is unreachable.
"""
import os, json
try:
    import urllib.request as _ur
except Exception:
    _ur = None

OLLAMA = os.environ.get('OLLAMA_URI', 'http://127.0.0.1:11434')


def respond(persona: dict, prompt: str, model: str | None = None) -> str:
    """Call local Ollama /api/generate with persona/model. Returns raw text or error message."""
    model_name = model or persona.get('model') or persona.get('id') or 'tinyllama:latest'
    payload = json.dumps({"model": model_name, "prompt": prompt}).encode('utf-8')
    if _ur is None:
        return f"[thoth client: urllib not available]"
    try:
        req = _ur.Request(OLLAMA + '/api/generate', data=payload, headers={'Content-Type': 'application/json'})
        with _ur.urlopen(req, timeout=120) as resp:
            return resp.read().decode('utf-8')
    except Exception as e:
        return f"[thoth client error: {e}]"
