import sqlite3
import json
import logging
from datetime import datetime
from typing import Dict, Any, List
from janebot_motherbrain.agents.base_agent import BaseAgent, AgentType, AgentStatus
from OllamaWrapper.client import OllamaWrapper

logger = logging.getLogger(__name__)

class StrategicAnalysisAgent(BaseAgent):
    """
    Strategic Analysis Agent: Persistent memory, market analyst, and brain for 
    business pain-point projection.
    """
    
    def __init__(self, name: str = "StratAnalyst"):
        super().__init__(
            name=name,
            agent_type=AgentType.ANALYTICS,
            description="Analyzes market data for pain-point projection and business model generation.",
            capabilities=["analyze_pain_points", "generate_business_models"],
            max_concurrent=1
        )
        self.db_path = f"data/{self.agent_id}.db"
        self.brain = OllamaWrapper()
        self._init_db()

    def _init_db(self):
        """Persistent storage for analysis history."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY,
                timestamp DATETIME,
                topic TEXT,
                insights TEXT,
                mode TEXT
            )
        """)
        conn.commit()
        conn.close()

    async def execute(self, capability: str, payload: Dict[str, Any]) -> Any:
        """Route capabilities to cognitive processing."""
        if capability == "analyze_pain_points":
            return await self._analyze_pain_points(payload)
        elif capability == "generate_business_models":
            return await self._generate_models(payload)
        return {"error": "Capability not implemented"}

    async def _query_ollama(self, prompt: str) -> str:
        """Integration with local Ollama instance for reasoning."""
        return await self.brain.query(prompt)

    async def _analyze_pain_points(self, data: Dict[str, Any]) -> Dict[str, Any]:
        mode = self.operational_state.get('decision_mode', 'BLUE')
        prompt = f"Analyze these business pain points under {mode} hat: {json.dumps(data)}"
        insight = await self._query_ollama(prompt)
        
        # Save to memory
        conn = sqlite3.connect(self.db_path)
        conn.execute("INSERT INTO analysis_history (timestamp, topic, insights, mode) VALUES (?, ?, ?, ?)",
                     (datetime.now(), "pain_points", insight, mode))
        conn.commit()
        conn.close()
        return {"insight": insight}

    async def _generate_models(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {"model": "Dynamic AI-Boardroom Pivot Model"}

    async def on_state_change(self, new_state: Dict[str, Any]):
        """Agent updates internal context when mode changes."""
        logger.info(f"SAA shifting focus to: {new_state.get('decision_mode')}")
