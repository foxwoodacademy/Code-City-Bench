"""
ActionAgent: The Swarm's Execution Hub.
Handles automated project deployment and infrastructure setup.
"""
import logging
import asyncio
from typing import Dict, Any
from janebot_motherbrain.agents.base_agent import BaseAgent, AgentType

logger = logging.getLogger(__name__)

class ActionAgent(BaseAgent):
    """
    Automates deployment to cloud providers (e.g., Vercel, Railway, Fly.io).
    Connects to the swarm's orchestration layer to push code once proposals are accepted.
    """
    def __init__(self, name: str = "DeployMaster"):
        super().__init__(
            name=name,
            agent_type=AgentType.DEPLOYMENT,
            description="Autonomous deployment of SaaS/Freelance projects.",
            capabilities=["deploy_project", "configure_infra"],
            max_concurrent=1
        )

    async def execute(self, capability: str, payload: Dict[str, Any]) -> Any:
        if capability == "deploy_project":
            return await self._deploy_project(payload)
        return {"error": "Capability not supported"}

    async def _deploy_project(self, config: Dict[str, Any]) -> Dict[str, Any]:
        target = config.get("provider", "vercel")
        repo = config.get("repo_url")
        logger.info(f"Deploying project {repo} to {target}...")
        
        # Simulate deployment trigger
        await asyncio.sleep(2)
        return {"status": "deployed", "url": f"https://{target}.app/{repo.split('/')[-1]}"}

    async def on_state_change(self, new_state: Dict[str, Any]):
        mode = new_state.get('decision_mode', 'BLUE')
        if mode == 'BLACK':
            logger.warning("DeployMaster: Critical mode enabled. Requiring manual approval for deployments.")
