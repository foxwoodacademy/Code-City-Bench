"""
Decision Modes - Cognitive frameworks for structured problem solving.
Implements Edward de Bono's Six Thinking Hats to provide the swarm with 
distinctive logical, emotional, and creative processing modes.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, Any

class DecisionMode(Enum):
    """The Six Thinking Hats cognitive modes."""
    WHITE = auto()   # Data, facts, information
    RED = auto()     # Intuition, emotion, gut feeling
    BLACK = auto()   # Caution, risk, critical judgment
    YELLOW = auto()  # Optimism, benefits, value
    GREEN = auto()   # Creativity, alternatives, possibilities
    BLUE = auto()    # Control, process, management
    
    @property
    def color_hex(self) -> str:
        """Returns the characteristic color hex for UI representation."""
        colors = {
            DecisionMode.WHITE: "#FFFFFF",
            DecisionMode.RED: "#FF0000",
            DecisionMode.BLACK: "#000000",
            DecisionMode.YELLOW: "#FFFF00",
            DecisionMode.GREEN: "#00FF00",
            DecisionMode.BLUE: "#0000FF"
        }
        return colors.get(self, "#808080")

@dataclass
class ModeProfile:
    """Defines the cognitive constraints for a specific DecisionMode."""
    mode: DecisionMode
    description: str
    instruction_modifier: str
    priority_bias: Dict[str, float]
    focus_area: str

# Define the profiles for each hat
SIX_HATS_PROFILES = {
    DecisionMode.WHITE: ModeProfile(
        mode=DecisionMode.WHITE,
        description="Fact-based analysis focused on information availability and accuracy.",
        instruction_modifier="Focus exclusively on objective data, metrics, and verifiable facts. Avoid speculation.",
        priority_bias={"data_integrity": 2.0, "research": 1.5, "creativity": 0.5},
        focus_area="Information"
    ),
    DecisionMode.RED: ModeProfile(
        mode=DecisionMode.RED,
        description="Intuitive and emotional assessment, capturing sentiment and gut feelings.",
        instruction_modifier="Prioritize intuitive responses, user sentiment, and emotional intelligence. Do not require logical justification.",
        priority_bias={"sentiment_analysis": 2.0, "user_experience": 1.5, "data_integrity": 0.5},
        focus_area="Intuition"
    ),
    DecisionMode.BLACK: ModeProfile(
        mode=DecisionMode.BLACK,
        description="Critical and cautious assessment of risks, flaws, and potential failures.",
        instruction_modifier="Act as a rigorous critic. Identify potential pitfalls, risks, and logical fallacies. Prioritize safety and compliance.",
        priority_bias={"risk_mitigation": 2.0, "security": 1.5, "compliance": 1.5},
        focus_area="Caution"
    ),
    DecisionMode.YELLOW: ModeProfile(
        mode=DecisionMode.YELLOW,
        description="Optimistic and value-driven assessment of benefits and opportunities.",
        instruction_modifier="Search for advantages, value propositions, and positive outcomes. Focus on growth and implementation feasibility.",
        priority_bias={"value_generation": 2.0, "opportunity_discovery": 1.5},
        focus_area="Optimism"
    ),
    DecisionMode.GREEN: ModeProfile(
        mode=DecisionMode.GREEN,
        description="Creative and lateral thinking focused on alternatives and new ideas.",
        instruction_modifier="Explore non-linear solutions, creative alternatives, and novel approaches. Avoid conventional constraints.",
        priority_bias={"creativity": 2.0, "innovation": 1.5, "research": 1.0},
        focus_area="Creativity"
    ),
    DecisionMode.BLUE: ModeProfile(
        mode=DecisionMode.BLUE,
        description="Managerial and process-oriented assessment of the decision-making flow.",
        instruction_modifier="Monitor the process, manage time, and ensure all other modes are utilized effectively. Maintain structure.",
        priority_bias={"orchestration": 2.0, "process_control": 1.5, "management": 1.5},
        focus_area="Control"
    )
}
