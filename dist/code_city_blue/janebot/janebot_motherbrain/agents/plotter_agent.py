"""
Plotter Agent - Visualization generation for boardroom readiness.
Transforms JSON prediction data into clean, minimalist SVG/PNG charts.
"""

import logging
from typing import Dict, Any
import matplotlib.pyplot as plt
import io
import base64
from janebot_motherbrain.agents.base_agent import BaseAgent, AgentType

logger = logging.getLogger(__name__)

class PlotterAgent(BaseAgent):
    """
    Automated visualization agent. Generates charts from analytics output.
    """
    
    def __init__(self, name: str = "ChartMaster"):
        super().__init__(
            name=name,
            agent_type=AgentType.ANALYTICS,
            description="Generates visual charts from market forecasts.",
            capabilities=["generate_chart"],
            max_concurrent=1
        )

    async def execute(self, capability: str, payload: Dict[str, Any]) -> Any:
        if capability == "generate_chart":
            return await self._generate_plot(payload)
        return {"error": "Capability not supported"}

    async def _generate_plot(self, plot_data: Dict[str, Any]) -> str:
        """Generates a base64 encoded PNG chart."""
        plt.figure(figsize=(8, 4))
        plt.plot(plot_data.get('x', []), plot_data.get('y', []), marker='o')
        plt.title(plot_data.get('title', 'Market Forecast'))
        plt.grid(True)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        
        return img_str
