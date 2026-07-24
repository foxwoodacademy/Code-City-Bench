"""Consenting, aggregate, or authorized human movement pattern events."""

DOMAIN = "movement"
DESCRIPTION = "Movement-pattern indexing for consenting or aggregate datasets."

EVENTS = {
    "path_observed": "movement.path.observed",
    "pattern_indexed": "movement.pattern.indexed",
    "deviation_detected": "movement.deviation.detected",
    "privacy_review": "movement.privacy.review",
}

PERSONA = {
    "name": "Movement Pattern Analyst",
    "prompt_template": (
        "Given these movement and system events, identify the clearest aggregate "
        "pattern or anomaly while preserving privacy and avoiding identity claims. "
        "Respond in one sentence."
    ),
    "location": "analyst.movement",
    "source": "analyst_movement",
    "event_key": "pattern_indexed",
}

