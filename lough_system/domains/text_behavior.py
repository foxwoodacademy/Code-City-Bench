"""Text and language-pattern analysis events with uncertainty controls."""

DOMAIN = "text_behavior"
DESCRIPTION = "Language-pattern and discourse analysis without lie-detection claims."

EVENTS = {
    "language_marker": "text_behavior.language.marker",
    "discourse_shift": "text_behavior.discourse.shift",
    "uncertainty_flag": "text_behavior.uncertainty.flag",
    "review_required": "text_behavior.review.required",
}

PERSONA = {
    "name": "Text Behavior Analyst",
    "prompt_template": (
        "Given these text-behavior and system events, identify the clearest "
        "language-pattern shift and uncertainty. Do not claim deception detection. "
        "Respond in one sentence."
    ),
    "location": "analyst.text_behavior",
    "source": "analyst_text_behavior",
    "event_key": "uncertainty_flag",
}

