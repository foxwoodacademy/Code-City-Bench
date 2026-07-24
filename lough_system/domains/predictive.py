"""Predictive modeling lifecycle events."""

DOMAIN = "predictive"
DESCRIPTION = "Model training, scoring, drift, and validation events."

EVENTS = {
    "dataset_ingested": "predictive.dataset.ingested",
    "model_trained": "predictive.model.trained",
    "score_generated": "predictive.score.generated",
    "drift_detected": "predictive.drift.detected",
    "validation_result": "predictive.validation.result",
}

PERSONA = {
    "name": "Predictive Model Analyst",
    "prompt_template": (
        "Given these predictive-modeling and system events, identify the most "
        "important model quality, drift, or validation issue. Respond in one sentence."
    ),
    "location": "analyst.predictive",
    "source": "analyst_predictive",
    "event_key": "validation_result",
}

