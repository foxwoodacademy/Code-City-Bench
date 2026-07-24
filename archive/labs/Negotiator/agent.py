"""
Negotiator Agent: The closer.
Transforms lead data into high-converting, personalized proposals.
"""
import logging
from typing import Dict, Any
from janebot_motherbrain.agents.base_agent import BaseAgent, AgentType

logger = logging.getLogger(__name__)

class Negotiator(BaseAgent):
    def __init__(self):
        super().__init__(name="Negotiator", agent_type=AgentType.LLM)
        self.capabilities = ["draft_proposal", "negotiate_terms"]

    async def execute(self, capability: str, payload: Dict[str, Any]) -> Any:
        if capability == "draft_proposal":
            return await self._draft_proposal(payload)
        return {"error": "Capability not supported"}

    async def _draft_proposal(self, lead_data: Dict[str, Any]) -> str:
        # Reflect persona and hat in the proposal tone
        persona = self.operational_state.get('persona_name', 'JaneBot')
        hat = self.operational_state.get('decision_mode', 'BLUE')
        
        proposal = f"Drafting proposal for: {lead_data.get('title')} using {persona} approach in {hat} mode."
        logger.info(proposal)
        return proposal
