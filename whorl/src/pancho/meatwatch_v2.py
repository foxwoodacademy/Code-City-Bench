"""
MEATWATCH -- constraint parser and conditional agent dispatcher for Pancho Villa.

Instead of firing all 9 agents in parallel regardless of what the prompt asks,
MEATWATCH listens to the initial prompt, extracts constraints (deploy targets,
compatibility requirements, documentation needs, etc.), and tells Pancho which
agents to actually invoke and in what order.

The core idea: one prompt input, surgical agent selection, no wasted cycles.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Agent(str, Enum):
    """The 9 agents in the Pancho Villa stack."""
    GEMINI = "gemini"          # script generation
    FREEBUFF = "freebuff"      # security/JS attack vectors
    VIBE = "vibe"              # frontend (React Native)
    PYTCH = "pytch"            # documentation
    VERTICAL_AI = "vertical-ai"  # analysis & refinement
    DNA = "dna"                # timeline & roadmap
    MOLT = "molt"              # refinement & supervision
    FRONT_DESK = "front-desk"  # pricing & tiers
    ZEROCLAW = "zeroclaw"      # deployment


class DeployTarget(str, Enum):
    """Known deployment targets."""
    RENDER = "render"
    RAILWAY = "railway"
    HEROKU = "heroku"
    VERCEL = "vercel"
    NETLIFY = "netlify"
    DOCKER = "docker"
    TERMUX = "termux"
    LOCAL = "local"


@dataclass
class Constraint:
    """A parsed constraint from the user prompt."""
    key: str
    value: str
    confidence: float  # 0.0-1.0, how sure we are about this extraction


@dataclass
class DeploymentPlan:
    """The result of constraint parsing: what to actually do."""
    # agent execution
    agents: list[Agent] = field(default_factory=list)
    agent_order: list[Agent] = field(default_factory=list)  # if order matters
    
    # deployment
    deploy_target: Optional[DeployTarget] = None
    deploy_immediately: bool = False
    
    # constraints
    compatibility: list[str] = field(default_factory=list)  # "plays well with X"
    needs_frontend: bool = False
    needs_documentation: bool = False
    needs_database: Optional[str] = None  # sqlite, postgres, mongo
    needs_security_review: bool = False
    
    # metadata
    all_constraints: list[Constraint] = field(default_factory=list)
    raw_prompt: str = ""
    confidence: float = 0.0  # overall confidence in the plan


# Signal patterns: (regex, agent(s) to include, key, value_extractor)
# value_extractor is a callable that takes the regex match and returns the value
_SIGNALS: list[tuple[re.Pattern, list[Agent], str, callable]] = [
    # backend generation -> GEMINI
    (re.compile(r"python\s+backend|write\s+a\s+python|backend\s+code", re.I),
     [Agent.GEMINI], "backend_type", lambda m: "python"),
    
    # frontend needs -> VIBE
    (re.compile(r"react\s+native|frontend|ui\s+component|vibe", re.I),
     [Agent.VIBE], "frontend_type", lambda m: "react-native"),
    
    # security/hacking -> FREEBUFF
    (re.compile(r"security\s+review|vulnerability|attack\s+vector|pentest|exploit", re.I),
     [Agent.FREEBUFF], "security_mode", lambda m: "enabled"),
    
    # documentation -> PYTCH
    (re.compile(r"documentation|docs|readme|spec|architecture", re.I),
     [Agent.PYTCH], "documentation", lambda m: "yes"),
    
    # deployment -> ZEROCLAW (+ FRONT_DESK if pricing needed)
    (re.compile(r"deploy(?:ment)?|ship|go\s+live|launch|production", re.I),
     [Agent.ZEROCLAW], "deploy_phase", lambda m: "enabled"),
    
    # deploy target
    (re.compile(r"deploy\s+to\s+(render|railway|heroku|vercel|netlify|docker|termux|local)", re.I),
     [Agent.ZEROCLAW], "deploy_target", lambda m: m.group(1).lower()),
    
    # compatibility constraints
    (re.compile(r"plays\s+well\s+with\s+(\w+)|compatible\s+with\s+(\w+)|integr[a-z]*\s+with\s+(\w+)", re.I),
     [Agent.VERTICAL_AI], "compatibility", lambda m: next(g for g in m.groups() if g)),
    
    # database choice
    (re.compile(r"(sqlite|postgres|mongodb|mysql)\s+database|database:\s*(sqlite|postgres|mongodb|mysql)", re.I),
     [Agent.DNA], "database", lambda m: m.group(1) or m.group(2)),
    
    # analysis & refinement
    (re.compile(r"analyze|refine|improve|optimize|review", re.I),
     [Agent.VERTICAL_AI], "analysis_phase", lambda m: "enabled"),
    
    # process supervision & refinement
    (re.compile(r"supervise|watch|monitor|refine|polish", re.I),
     [Agent.MOLT], "supervision", lambda m: "enabled"),
    
    # timeline & roadmap
    (re.compile(r"timeline|roadmap|schedule|phases|plan", re.I),
     [Agent.DNA], "timeline", lambda m: "enabled"),
    
    # pricing & commercialization
    (re.compile(r"pricing|price|tier|cost|commercial|sell|package", re.I),
     [Agent.FRONT_DESK], "pricing_phase", lambda m: "enabled"),
]


def parse_constraints(prompt: str) -> DeploymentPlan:
    """
    Parse a user prompt and extract constraints that determine which agents
    to fire and in what order.
    
    Args:
        prompt: The raw user input (the Pancho Villa initial prompt)
    
    Returns:
        A DeploymentPlan with agents to execute, deploy target, and metadata.
    """
    plan = DeploymentPlan(raw_prompt=prompt)
    agents_set = set()
    
    # walk the signal patterns
    for pattern, agent_list, key, extractor in _SIGNALS:
        matches = list(pattern.finditer(prompt))
        if matches:
            for match in matches:
                try:
                    value = extractor(match)
                    constraint = Constraint(key=key, value=value, confidence=0.8)
                    plan.all_constraints.append(constraint)
                    agents_set.update(agent_list)
                    
                    # set specific flags based on the constraint
                    if key == "frontend_type":
                        plan.needs_frontend = True
                    elif key == "documentation":
                        plan.needs_documentation = True
                    elif key == "database":
                        plan.needs_database = value
                    elif key == "security_mode":
                        plan.needs_security_review = True
                    elif key == "deploy_target":
                        try:
                            plan.deploy_target = DeployTarget[value.upper()]
                        except KeyError:
                            pass
                    elif key == "compatibility":
                        plan.compatibility.append(value)
                except Exception:
                    pass
    
    # implicit rules: if we're deploying, we probably need MOLT to supervise
    if Agent.ZEROCLAW in agents_set:
        plan.deploy_immediately = True
        agents_set.add(Agent.MOLT)
    
    # if frontend is needed but no backend was explicitly mentioned, add GEMINI
    if plan.needs_frontend and Agent.GEMINI not in agents_set:
        agents_set.add(Agent.GEMINI)
    
    # if we're building anything, VERTICAL_AI should review for consistency
    if len(agents_set) > 1 and Agent.VERTICAL_AI not in agents_set:
        agents_set.add(Agent.VERTICAL_AI)
    
    # ordering: establish a sensible execution order
    # (some agents need output from others)
    preferred_order = [
        Agent.GEMINI,       # backend first
        Agent.VIBE,         # frontend second
        Agent.PYTCH,        # docs can run parallel to above
        Agent.FREEBUFF,     # security review in parallel
        Agent.VERTICAL_AI,  # analysis of what was built
        Agent.DNA,          # timeline & roadmap
        Agent.MOLT,         # polish & supervise
        Agent.FRONT_DESK,   # pricing
        Agent.ZEROCLAW,     # deploy last
    ]
    
    plan.agents = list(agents_set)
    plan.agent_order = [a for a in preferred_order if a in agents_set]
    
    # confidence is high if we found explicit signals, lower if we had to infer
    if plan.all_constraints:
        plan.confidence = min(1.0, 0.5 + (len(plan.all_constraints) * 0.1))
    else:
        plan.confidence = 0.3  # low confidence, probably just a vague prompt
    
    return plan


def format_plan(plan: DeploymentPlan) -> str:
    """Human-readable summary of the execution plan."""
    lines = [
        "MEATWATCH EXECUTION PLAN",
        "=" * 50,
        f"Confidence: {plan.confidence:.0%}",
        "",
        "AGENTS TO INVOKE (in order):",
    ]
    
    for i, agent in enumerate(plan.agent_order, 1):
        lines.append(f"  {i}. {agent.value.upper()}")
    
    if plan.deploy_target:
        lines.append(f"\nDEPLOY TARGET: {plan.deploy_target.value}")
    
    if plan.compatibility:
        lines.append(f"COMPATIBILITY: {', '.join(plan.compatibility)}")
    
    if plan.needs_frontend:
        lines.append("✓ Frontend needed")
    if plan.needs_documentation:
        lines.append("✓ Documentation needed")
    if plan.needs_database:
        lines.append(f"✓ Database: {plan.needs_database}")
    if plan.needs_security_review:
        lines.append("✓ Security review enabled")
    
    if plan.all_constraints:
        lines.append("\nCONSTRAINTS DETECTED:")
        for c in plan.all_constraints:
            lines.append(f"  {c.key}: {c.value}")
    
    return "\n".join(lines)


# CLI for testing
if __name__ == "__main__":
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python meatwatch.py [--json] \"<prompt>\"")
        sys.exit(1)
    
    json_mode = False
    prompt_start = 1
    if sys.argv[1] == "--json":
        json_mode = True
        prompt_start = 2
    
    if len(sys.argv) <= prompt_start:
        print("Usage: python meatwatch.py [--json] \"<prompt>\"")
        sys.exit(1)
    
    prompt = " ".join(sys.argv[prompt_start:])
    plan = parse_constraints(prompt)
    
    if json_mode:
        output = {
            "agents": [a.value for a in plan.agent_order],
            "deploy_target": plan.deploy_target.value if plan.deploy_target else None,
            "deploy_immediately": plan.deploy_immediately,
            "confidence": plan.confidence,
            "compatibility": plan.compatibility,
            "needs_frontend": plan.needs_frontend,
            "needs_documentation": plan.needs_documentation,
            "needs_database": plan.needs_database,
            "needs_security_review": plan.needs_security_review,
            "constraints": [
                {"key": c.key, "value": c.value, "confidence": c.confidence}
                for c in plan.all_constraints
            ],
        }
        print(json.dumps(output, indent=2))
    else:
        print(format_plan(plan))
