"""
domain_bridge.py
Convenience helpers for emitting events by domain and event key.
"""

import field_bridge
import event_registry


def emit_domain_event(
    domain,
    event_key,
    intensity=1.0,
    location="system",
    payload=None,
    source="unknown",
    relation_id=None,
    confidence=None,
    provenance=None,
    review_status=None,
    created_by=None,
):
    """Emit an event using a registered domain name and event key."""
    events = event_registry.get_domain_events(domain)
    if not events:
        raise ValueError(f"Unknown domain: {domain}")
    if event_key not in events:
        known = ", ".join(sorted(events.keys()))
        raise ValueError(f"Unknown event key for {domain}: {event_key}. Known: {known}")

    return field_bridge.emit(
        event_type=events[event_key],
        intensity=intensity,
        location=location,
        payload=payload or {},
        source=source,
        relation_id=relation_id,
        confidence=confidence,
        provenance=provenance,
        review_status=review_status,
        created_by=created_by,
    )


def list_domains():
    """Return all registered domains and event keys."""
    return {
        domain: sorted(events.keys())
        for domain, events in event_registry.all_namespaces().items()
    }
