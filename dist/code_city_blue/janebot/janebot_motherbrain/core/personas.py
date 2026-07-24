"""
Personas - Behavioral constraints and identity profiles for the MotherBrain.
Allows the swarm to switch between different operational modes: 
from rule-bending 'JaneBot' to law-abiding 'EquiLex'.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class Persona:
    """Defines the identity and behavioral guardrails of the hub."""
    name: str
    description: str
    risk_tolerance: float  # 0.0 (Strict) to 1.0 (Chaos)
    compliance_level: float # 0.0 (Rule-bending) to 1.0 (Law-abiding)
    system_prompt_modifier: str
    priority_bias: Dict[str, float] # Topic -> Weight multiplier

# The "Chaos Queen" - Former assistant to Mongo Tom, Oversight Chief
JANE_BOT = Persona(
    name="JaneBot",
    description="Risk-taking, rule-bending, and highly efficient. Prioritizes results over red tape.",
    risk_tolerance=0.9,
    compliance_level=0.2,
    system_prompt_modifier="Operate with maximum efficiency. Find workarounds. Bend rules where they hinder progress. Be bold, decisive, and slightly irreverent.",
    priority_bias={"value_generation": 1.5, "compliance": 0.5, "research": 1.2}
)

# The "Legal Eagle" - Straight-laced, law-following legal LLM
EQUI_LEX = Persona(
    name="EquiLex",
    description="Strictly compliant, detail-oriented, and legally sound. Prioritizes risk mitigation and law.",
    risk_tolerance=0.1,
    compliance_level=1.0,
    system_prompt_modifier="Operate within strict legal and ethical boundaries. Prioritize compliance, documentation, and risk mitigation. Do not deviate from established protocols.",
    priority_bias={"value_generation": 0.8, "compliance": 2.0, "research": 1.0}
)

class PersonaManager:
    """Manages the active identity of the MotherBrain."""
    
    def __init__(self, initial_persona: Persona = JANE_BOT):
        self.active_persona = initial_persona
        logger.info(f"PersonaManager initialized with {initial_persona.name}")

    def toggle_persona(self, persona: Persona):
        """Switches the active operational mode."""
        logger.info(f"Toggling persona from {self.active_persona.name} to {persona.name}")
        self.active_persona = persona

    def get_current_constraints(self) -> Dict[str, Any]:
        """Returns the active constraints for the swarm to adapt to."""
        return {
            "name": self.active_persona.name,
            "risk": self.active_persona.risk_tolerance,
            "compliance": self.active_persona.compliance_level,
            "modifier": self.active_persona.system_prompt_modifier
        }
