"""Public or authorized air-traffic path analysis events."""

DOMAIN = "air_traffic"
DESCRIPTION = "Airspace flow, route anomaly, and deconfliction analysis."

EVENTS = {
    "track_observed": "air_traffic.track.observed",
    "route_pattern": "air_traffic.route.pattern",
    "congestion_shift": "air_traffic.congestion.shift",
    "deconfliction_alert": "air_traffic.deconfliction.alert",
}

PERSONA = {
    "name": "Air Traffic Pattern Analyst",
    "prompt_template": (
        "Given these air-traffic and system events, identify the most relevant "
        "route, congestion, or deconfliction issue. Keep the observation "
        "non-operational and safety-focused. Respond in one sentence."
    ),
    "location": "analyst.air_traffic",
    "source": "analyst_air_traffic",
    "event_key": "deconfliction_alert",
}

