"""Safety, compliance, and human-rights governance events for high-risk systems."""

DOMAIN = "safety_governance"
DESCRIPTION = (
    "Audit, compliance, human-rights, and simulation-only oversight for high-risk systems."
)

EVENTS = {
    "policy_review": "safety_governance.policy.review",
    "human_rights_check": "safety_governance.human_rights.check",
    "simulation_boundary": "safety_governance.simulation.boundary",
    "operator_accountability": "safety_governance.operator.accountability",
    "misuse_risk": "safety_governance.misuse.risk",
    "escalation_blocked": "safety_governance.escalation.blocked",
}

PERSONA = {
    "name": "Safety Governance Analyst",
    "prompt_template": (
        "Given these safety-governance and system events, identify the most "
        "important audit, accountability, human-rights, or misuse-risk issue. "
        "Keep the observation non-operational and compliance-focused. Respond in one sentence."
    ),
    "location": "analyst.safety_governance",
    "source": "analyst_safety_governance",
    "event_key": "misuse_risk",
}

