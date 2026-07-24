"""
Passive Income Simulation - A logged workflow demonstrating value generation using ZeroClaw.
This script simulates how a ModMind swarm can be orchestrated to generate passive income.
"""

import asyncio
import logging
import uuid
from datetime import datetime
from janebot_motherbrain.core.motherbrain import MotherBrain, SwarmConfig
from janebot_motherbrain.core.task_queue import Priority, Task
from janebot_motherbrain.core.personas import JANE_BOT, EQUI_LEX, Persona
from janebot_motherbrain.core.decision_modes import DecisionMode

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("IncomeSim")

async def simulate_value_stream():
    # 1. Setup MotherBrain as the Hub
    config = SwarmConfig(swarm_name="IncomeGenerator_Alpha")
    hub = MotherBrain(config)
    await hub.start()
    
    logger.info("--- INITIALIZING PASSIVE INCOME WORKFLOW ---")
    logger.info(f"Active Persona: {hub.state_manager.current_state.persona.name}, Mode: {hub.state_manager.current_state.decision_mode.name}")
    
    # 2. Define the Value Generation Pipeline
    # Pipeline: Market Analysis -> Signal Generation -> Automated Execution -> Audit
    pipeline = [
        {"desc": "Scan crypto markets for arbitrage gaps", "cap": "market_analyzer", "prio": Priority.HIGH},
        {"desc": "Generate high-confidence trading signals", "cap": "signal_generator", "prio": Priority.HIGH},
        {"desc": "Execute micro-trades via API", "cap": "trade_executor", "prio": Priority.CRITICAL},
        {"desc": "Audit trade logs for compliance/tax", "cap": "legal_auditor", "prio": Priority.LOW},
    ]
    
    # 3. Simulate Execution
    try:
        for step in pipeline:
            logger.info(f"Dispatching: {step['desc']} (Priority: {step['prio'].name})")
            task_id = await hub.submit_task(
                description=step['desc'],
                capability=step['cap'],
                priority=step['prio']
            )
            logger.info(f"Task {task_id} is now flowing through the ZeroClaw fabric...")
            await asyncio.sleep(1) # Simulate network latency
            
        # 4. Demonstrate the Persona Toggle and Decision Modes
        logger.info("--- SCENARIO: REGULATORY SCRUTINY DETECTED ---")
        await hub.set_decision_mode(DecisionMode.BLACK) # Adopt a cautious mode
        await hub.toggle_persona(EQUI_LEX) # Switch to Legal Eagle persona
        logger.info(f"Swarm switched to {hub.state_manager.current_state.persona.name} mode (Decision Mode: {hub.state_manager.current_state.decision_mode.name}). Risk tolerance dropped to {hub.state_manager.current_state.persona.risk_tolerance}.")
        
        logger.info("Executing Compliance Audit...")
        await hub.submit_task("Full audit of all generated income streams", "legal_auditor", priority=Priority.CRITICAL)
        
        # 5. Switch back to JaneBot for growth
        logger.info("--- SCENARIO: CLEARANCE RECEIVED. RESUMING GROWTH ---")
        await hub.set_decision_mode(DecisionMode.YELLOW) # Adopt an optimistic mode
        await hub.toggle_persona(JANE_BOT) # Switch back to JaneBot persona
        logger.info(f"Swarm switched back to {hub.state_manager.current_state.persona.name} (Decision Mode: {hub.state_manager.current_state.decision_mode.name}). Let's get this bread.")
        
        await hub.submit_task("Aggressive expansion into new arbitrage markets", "market_analyzer", priority=Priority.HIGH)
        
    finally:
        await hub.stop()
        logger.info("--- SIMULATION COMPLETE ---")

if __name__ == "__main__":
    asyncio.run(simulate_value_stream())
