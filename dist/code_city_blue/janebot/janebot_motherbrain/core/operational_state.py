"""
Operational State Management - Unified control of Identity and Cognitive Modes.
Provides a single source of truth for the MotherBrain's current behavioral 
and decision-making state, ensuring consistency and seamless transitions.
"""

import asyncio
import logging
from dataclasses import dataclass
from typing import Dict, Any, Optional, Callable

from .personas import Persona, JANE_BOT, EQUI_LEX
from .decision_modes import DecisionMode, SIX_HATS_PROFILES, ModeProfile

logger = logging.getLogger(__name__)

@dataclass
class OperationalState:
    """The complete behavioral profile of the MotherBrain at a point in time."""
    persona: Persona
    decision_mode: DecisionMode
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "persona_name": self.persona.name,
            "decision_mode": self.decision_mode.name,
            "risk_tolerance": self.persona.risk_tolerance,
            "compliance_level": self.persona.compliance_level,
            "instruction_modifier": f"{self.persona.system_prompt_modifier} {SIX_HATS_PROFILES[self.decision_mode].instruction_modifier}"
        }

class OperationalStateManager:
    """
    Manages the transition and broadcast of the MotherBrain's operational state.
    
    This manager is responsible for:
    1. Maintaining the current 'OperationalState'.
    2. Handling transitions between personas and decision modes.
    3. Broadcasting state changes to the swarm via the MessageBus.
    """
    
    def __init__(self, message_bus, initial_persona: Persona = JANE_BOT, initial_mode: DecisionMode = DecisionMode.BLUE):
        self._message_bus = message_bus
        self._current_state = OperationalState(persona=initial_persona, decision_mode=initial_mode)
        self._lock = asyncio.Lock()
        self._on_state_change_callbacks: Dict[str, list[Callable]] = {}
        logger.info(f"OperationalStateManager initialized: Persona={initial_persona.name}, Mode={initial_mode.name}")

    @property
    def current_state(self) -> OperationalState:
        return self._current_state

    async def set_persona(self, persona: Persona):
        """Changes the active persona and triggers a state change broadcast."""
        async with self._lock:
            if self._current_state.persona == persona:
                return
            
            old_persona = self._current_state.persona
            self._current_state = OperationalState(
                persona=persona,
                decision_mode=self._current_state.decision_mode
            )
            logger.info(f"OperationalState: Persona changed from {old_persona.name} to {persona.name}")
            await self._broadcast_state_change()

    async def set_decision_mode(self, mode: DecisionMode):
        """Changes the active decision mode and triggers a state change broadcast."""
        async with self._lock:
            if self._current_state.decision_mode == mode:
                return
            
            old_mode = self._current_state.decision_mode
            self._current_state = OperationalState(
                persona=self._current_state.persona,
                decision_mode=mode
            )
            logger.info(f"OperationalState: DecisionMode changed from {old_mode.name} to {mode.name}")
            await self._broadcast_state_change()

    async def _broadcast_state_change(self):
        """Broadcasts the new operational state to the entire swarm."""
        if self._message_bus:
            from .message_bus import Message, MessageType
            msg = Message(
                sender="motherbrain.state_manager",
                topic="system.operational_state_change",
                message_type=MessageType.BROADCAST,
                payload=self._current_state.to_dict()
            )
            await self._message_bus.broadcast(msg)
            
        # Trigger local callbacks
        for callback in self._on_state_change_callbacks.get("change", []):
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(self._current_state)
                else:
                    callback(self._current_state)
            except Exception as e:
                logger.error(f"Error in state change callback: {e}")

    def subscribe(self, event: str, callback: Callable):
        """Registers a callback for state change events."""
        if event not in self._on_state_change_callbacks:
            self._on_state_change_callbacks[event] = []
        self._on_state_change_callbacks[event].append(callback)

    def get_full_context(self) -> Dict[str, Any]:
        """Returns a comprehensive view of the current operational constraints."""
        state = self._current_state
        persona = state.persona
        mode_profile = SIX_HATS_PROFILES[state.decision_mode]
        
        return {
            "persona": persona.__dict__,
            "decision_mode": state.decision_mode.name,
            "mode_profile": mode_profile.__dict__,
            "combined_modifier": state.to_dict()["instruction_modifier"]
        }
