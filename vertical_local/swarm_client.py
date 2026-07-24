"""Swarm client stub
Provides scout_respond integration point. Default: call scout_sandbox.scout_respond when available.
"""
try:
    from scout_sandbox import scout_respond as _scout
except Exception:
    _scout = None


def scout_respond(persona: dict, prompt: str) -> str:
    if _scout is None:
        return "[swarm client: scout_sandbox unavailable — no real scouts configured]"
    try:
        return _scout(persona=persona, prompt=prompt, rng=None)
    except Exception as e:
        return f"[swarm client error: {e}]"
