import random

# A deterministic sandbox responder that gives persona-flavored replies.

_FRAMES = [
    "As the {role}, I would focus on {focus} and recommend {rec}.",
    "From a {role} perspective: {rec}. Key risk: {risk}.",
    "The core problem is {problem}. My move: {rec}.",
]

FOCUS_POOL = ["cost reduction", "market expansion", "operational resilience", "data strategy", "customer retention"]
RECS = ["pilot a focused feature", "reallocate budget to growth channels", "standardize processes", "invest in automation", "conduct customer research"]
RISKS = ["execution risk", "timing risk", "regulatory concerns", "technical debt", "market saturation"]
PROBLEMS = ["poor product-market fit", "fragmented data", "lack of alignment", "unstable margins", "low retention"]


def scout_respond(persona: dict, prompt: str, rng: random.Random | None = None) -> str:
    rng = rng or random.Random()
    role = persona.get('role', 'Advisor')
    focus = rng.choice(FOCUS_POOL)
    rec = rng.choice(RECS)
    risk = rng.choice(RISKS)
    problem = rng.choice(PROBLEMS)
    frame = rng.choice(_FRAMES)
    return frame.format(role=role, focus=focus, rec=rec, risk=risk, problem=problem) + f"\n\n[Persona: {persona.get('name')}]"