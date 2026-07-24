"""
event_registry.py
Formal taxonomy for Lough System event namespaces.

Static core namespaces are kept for compatibility. Domain modules under
domains/ extend the registry without forcing every new use case into this file.
"""

import importlib
import pkgutil

# Behavioral Domain
BEHAVIOR_NAMESPACE = {
    "intent":     "behavior.intent.observed",
    "bias":       "behavior.pattern.cognitive_bias",
    "mental":     "behavior.state.mental_model",
    "deviation":  "behavior.deviation.action"
}

# Defense/DIB Domain
DIB_NAMESPACE = {
    "contract":   "dib.contract.lifecycle",
    "compliance": "dib.compliance.requirement",
    "fiscal":     "dib.fiscal.appropriation",
    "milestone":  "dib.milestone.performance"
}

# System Meta-Domain
SYSTEM_NAMESPACE = {
    "usage":      "system.usage",
    "error":      "system.error",
    "analyst":    "system.analyst.observation",
    "client":     "system.client.onboarded",
    "ingest":     "system.ingest.completed",
    "review":     "system.review.updated",
}

CORE_NAMESPACES = {
    "behavior": BEHAVIOR_NAMESPACE,
    "dib": DIB_NAMESPACE,
    "system": SYSTEM_NAMESPACE,
}


def load_domain_modules():
    """Load domain plugin modules from the local domains package."""
    try:
        import domains
    except ImportError:
        return {}

    loaded = {}
    for module_info in pkgutil.iter_modules(domains.__path__):
        module_name = f"domains.{module_info.name}"
        module = importlib.import_module(module_name)
        domain = getattr(module, "DOMAIN", module_info.name)
        events = getattr(module, "EVENTS", {})
        if events:
            loaded[domain] = module
    return loaded


DOMAIN_MODULES = load_domain_modules()
DOMAIN_NAMESPACES = {
    domain: getattr(module, "EVENTS", {})
    for domain, module in DOMAIN_MODULES.items()
}


def all_namespaces():
    """Return every registered namespace dictionary keyed by domain."""
    return {
        **CORE_NAMESPACES,
        **DOMAIN_NAMESPACES,
    }


def all_event_types():
    """Return a flat list of registered event type strings."""
    event_types = []
    for namespace in all_namespaces().values():
        event_types.extend(namespace.values())
    return event_types


def validate_event(event_type):
    """
    Check if an event_type belongs to a recognized namespace.
    Useful for filtering or upstream monitoring.
    """
    return event_type in all_event_types()


def get_domain_events(domain):
    """Return the event map for a domain, or an empty dict if unknown."""
    return all_namespaces().get(domain, {})


def get_personas():
    """Return analyst persona configs exposed by domain plugins."""
    personas = {}
    for domain, module in DOMAIN_MODULES.items():
        persona = getattr(module, "PERSONA", None)
        events = getattr(module, "EVENTS", {})
        if persona and events:
            event_key = persona.get("event_key")
            personas[domain] = {
                **persona,
                "event_type": events.get(event_key, next(iter(events.values()))),
                "relevant_event_types": list(events.values()) + [
                    SYSTEM_NAMESPACE["usage"],
                    SYSTEM_NAMESPACE["error"],
                ],
            }
    return personas
