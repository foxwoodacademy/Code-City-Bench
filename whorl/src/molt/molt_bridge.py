import os
from typing import Any, Dict
from src.molt.molt import MoltEngine

class MoltBridge:
    """
    Bridge to the Molt recursive improvement engine.
    Allows agents to trigger autonomous self-improvement.
    """
    
    def __init__(self):
        self.engine = MoltEngine()

    def improve_agent(self, agent_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invokes the Molt engine to refine agent logic and fitness parameters.
        """
        # Molt consumes the state and returns refined parameters/logic
        refined_state = self.engine.run_refinement(agent_state)
        return refined_state
