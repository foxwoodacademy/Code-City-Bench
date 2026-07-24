import asyncio
import pytest
from unittest.mock import MagicMock, AsyncMock
from janebot_motherbrain.core.operational_state import OperationalStateManager, OperationalState
from janebot_motherbrain.core.personas import JANE_BOT, EQUI_LEX
from janebot_motherbrain.core.decision_modes import DecisionMode

@pytest.mark.asyncio
async def test_state_transitions():
    mock_bus = AsyncMock()
    manager = OperationalStateManager(message_bus=mock_bus)
    
    # Test initial state
    assert manager.current_state.persona == JANE_BOT
    assert manager.current_state.decision_mode == DecisionMode.BLUE
    
    # Test persona change
    await manager.set_persona(EQUI_LEX)
    assert manager.current_state.persona == EQUI_LEX
    assert mock_bus.broadcast.called
    
    # Test decision mode change
    await manager.set_decision_mode(DecisionMode.BLACK)
    assert manager.current_state.decision_mode == DecisionMode.BLACK
    assert mock_bus.broadcast.call_count == 2
    
@pytest.mark.asyncio
async def test_callback_trigger():
    callback_triggered = False
    
    async def my_callback(state):
        nonlocal callback_triggered
        callback_triggered = True
        
    mock_bus = AsyncMock()
    manager = OperationalStateManager(message_bus=mock_bus)
    manager.subscribe("change", my_callback)
    
    await manager.set_persona(EQUI_LEX)
    assert callback_triggered
