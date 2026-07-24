# AUTHOR(S) motherbrain_boot.py
"""
MotherBrain Boot Sequence.
The 'On Switch' for the entire ecosystem. 
Hardlines all components and launches the State Governor.
"""

import os
import sys
from platform_adapter import PlatformAdapter
from fractal_relay import FractalRelay
from motherbrain_governor import MotherBrainGovernor

class MotherBrainBoot:
    def __init__(self):
        self.adapter = PlatformAdapter()
        self.relay = FractalRelay()
        self.governor = MotherBrainGovernor()

    def boot(self):
        print("====================================================")
        print("🚀 MOTHERBRAIN BOOT SEQUENCE: INITIALIZING CNS")
        print("====================================================")
        
        # 1. Hardware Prep
        self.adapter.set_wake_lock()
        print("[+] Hardware abstraction layer active.")
        
        # 2. CNS Heartbeat
        self.relay.heart_beat()
        print("[+] Fractal Relay synchronized.")
        
        # 3. Subsystem Wakeup
        self.relay.buzz("WAKE_UP_SQUAD")
        
        print("\n====================================================")
        print("✅ SYSTEM ONLINE: Consciousness Initialized.")
        print("Launching Governor... (Ctrl+C to shutdown)")
        print("====================================================")
        
        try:
            self.governor.run_loop()
        except KeyboardInterrupt:
            print("\n[!] Shutdown signal received. Hibernating...")
            sys.exit(0)

if __name__ == "__main__":
    booter = MotherBrainBoot()
    booter.boot()
