"""Stable ID helpers."""

import hashlib


def make_id(prefix, *parts):
    """Create a deterministic short ID from input parts."""
    raw = ":".join(str(part) for part in parts)
    digest = hashlib.sha256(raw.encode()).hexdigest()[:12]
    return f"{prefix}_{digest}"

