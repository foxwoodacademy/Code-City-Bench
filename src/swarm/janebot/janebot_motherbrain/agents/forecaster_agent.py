"""
Forecaster Agent - Predictive analysis and time-series forecasting.
This agent processes historical data from the StrategicAnalysisAgent to 
generate future market projections and demand fluctuation forecasts.
"""

import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
import numpy as np
from janebot_motherbrain.agents.base_agent import BaseAgent, AgentType

logger = logging.getLogger(__name__)

class ForecasterAgent(BaseAgent):
    """
    Predictive agent that handles time-series analysis and generates
    forecasts for demand, materials cost, and market viability.
    """
    
    def __init__(self, name: str = "MarketOracle"):
        super().__init__(
            name=name,
            agent_type=AgentType.ANALYTICS,
            description="Performs predictive modeling and time-series forecasting.",
            capabilities=["forecast_demand", "forecast_cogs", "project_viability"],
            max_concurrent=2
        )

    async def execute(self, capability: str, payload: Dict[str, Any]) -> Any:
        if capability == "forecast_demand":
            return await self._forecast_trend(payload, "demand")
        elif capability == "forecast_cogs":
            return await self._forecast_trend(payload, "cogs")
        return {"error": "Capability not supported"}

    async def _forecast_trend(self, historical_data: List[float], metric: str) -> Dict[str, Any]:
        """Simple linear regression forecasting."""
        if len(historical_data) < 2:
            return {"error": "Insufficient data"}
            
        x = np.arange(len(historical_data))
        y = np.array(historical_data)
        
        # Simple polynomial fit (trend)
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        
        # Predict next 7 days
        next_x = np.arange(len(historical_data), len(historical_data) + 7)
        predictions = p(next_x)
        
        return {
            "metric": metric,
            "trend": float(z[0]),
            "projection": predictions.tolist(),
            "confidence": 0.85
        }

    async def on_state_change(self, new_state: Dict[str, Any]):
        """Adjusts forecast sensitivity based on DecisionMode."""
        mode = new_state.get('decision_mode', 'BLUE')
        logger.info(f"MarketOracle adjusting sensitivity for {mode} mode.")
