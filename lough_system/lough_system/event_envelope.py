"""
event_envelope.py
Standard metadata envelope for Lough event payloads.
"""

import time

SCHEMA_VERSION = 1

REVIEW_REQUIRED_PREFIXES = (
    "safety_governance.",
    "movement.",
    "text_behavior.",
)


def default_review_status(event_type):
    """Return the default review status for an event type."""
    if event_type.startswith(REVIEW_REQUIRED_PREFIXES):
        return "review_required"
    return "unreviewed"


def normalize_payload(
    event_type,
    payload=None,
    source="unknown",
    confidence=None,
    provenance=None,
    review_status=None,
    created_by=None,
):
    """Attach the standard Lough metadata envelope to a payload."""
    if payload is None:
        payload = {}
    if not isinstance(payload, dict):
        payload = {"value": payload}

    normalized = dict(payload)
    existing = normalized.get("_lough", {})
    if not isinstance(existing, dict):
        existing = {}

    envelope = {
        "schema_version": SCHEMA_VERSION,
        "created_at": existing.get("created_at", time.time()),
        "created_by": created_by or existing.get("created_by") or source,
        "confidence": confidence if confidence is not None else existing.get("confidence", None),
        "provenance": provenance if provenance is not None else existing.get("provenance", {}),
        "review_status": review_status or existing.get("review_status") or default_review_status(event_type),
    }

    if not isinstance(envelope["provenance"], dict):
        envelope["provenance"] = {"note": str(envelope["provenance"])}

    normalized["_lough"] = envelope
    return normalized


def envelope_from_event(event):
    """Return the `_lough` envelope from a polled event."""
    payload = event.get("payload", {})
    if not isinstance(payload, dict):
        return {}
    envelope = payload.get("_lough", {})
    return envelope if isinstance(envelope, dict) else {}

