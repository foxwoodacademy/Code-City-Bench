# AUTHOR(S) motherbrain_governor.py
"""
MotherBrain Governor: The Consciousness.
Manages the global state of the RootBase ecosystem, transitioning 
between Production, Sentry, and Saturn modes.
"""

import time
import threading
from typing import Dict, Any
from platform_adapter import PlatformAdapter
from network_guard import NetworkGuard
from fractal_relay import FractalRelay
from whorl_runtime import WhorlRuntime

class MotherBrainGovernor:
    def __init__(self):
        self.adapter = PlatformAdapter()
        self.guard = NetworkGuard()
        self.relay = FractalRelay()
        self.whorl = WhorlRuntime()
        
        self.current_state = "MODE_OPEN"
        self.last_activity_time = time.time()
        self.is_running = True

    def run_loop(self):
        """
        The main consciousness loop.
        """
        print("[*] Governor active. Monitoring system state...")
        
        while self.is_running:
            # 1. Update Activity Timestamp
            # In a real implementation, this would be hooked into the Fractal Relay
            
            # 2. Evaluate State Transition
            self._evaluate_state()
            
            # 3. Execute State-Specific Logic
            self._execute_state_logic()
            
            time.sleep(10) # Heartbeat interval

    def _evaluate_state(self):
        """
        Determines the correct state based on network and activity.
        """
        connected, _ = self.guard.check_connectivity()
        idle_time = time.time() - self.last_activity_time
        
        # State Transition Logic
        if connected and self.guard.is_critical_sync:
            self._transition_to("MODE_SENTRY")
        elif idle_time > 300: # 5 minutes of silence
            self._transition_to("MODE_SATURN")
        elif not connected:
            self._transition_to("MODE_OPEN") # Default to local production
        else:
            self._transition_to("MODE_OPEN")

    def _transition_to(self, new_state: str):
        if self.current_state != new_state:
            print(f"[*] STATE TRANSITION: {self.current_state} -> {new_state}")
            self.current_state = new_state
            self.relay.buzz(f"STATE_CHANGE_{new_state}")

    def _execute_state_logic(self):
        """
        Triggers the behavior associated with the current state.
        """
        if self.current_state == "MODE_OPEN":
            # Maximum resource allocation to production agents
            pass
            
        elif self.current_state == "MODE_SENTRY":
            # Activate network guard and hold-position checks
            if self.guard.monitor_signal_fade():
                self.guard.trigger_hold_position()
                
        elif self.current_state == "MODE_SATURN":
            # Trigger the Saturn Engine's recursive sweep
            self._run_saturn_sweep()

    def _run_saturn_sweep(self):
        """
        Invokes the Whorl Runtime to perform maintenance.
        """
        print("[*] Entering Saturn Shift: Performing recursive maintenance...")
        sweep_pattern = {
            "name": "Saturn Root Sweep",
            "directives": [
                {
                    "type": "scan",
                    "path": ".",
                    "pattern": ".* (1).*|.*copy.*",
                    "action": "archive"
                }
            ]
        }
        self.whorl.execute_pattern(sweep_pattern)

    def update_activity(self):
        """Call this whenever an agent performs a task."""
        self.last_activity_time = time.time()

# -----------------------------------------------------------------------------
# LOWER CLASSES & HELPERS (The Boilerplate)
# -----------------------------------------------------------------------------

class StateMetadata:
    """Stores metadata about state transitions for behavioral analysis."""
    def __init__(self, state: str, enter_time: float):
        self.state = state
        self.enter_time = enter_time
