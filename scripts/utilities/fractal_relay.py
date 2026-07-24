# AUTHOR(S) fractal_relay.py
"""
Fractal Relay: The Central Nervous System (CNS).
Provides the hardline communication backbone for all RootBase subsystems.
Ensures that Code City, Vertical AI, aFiREfly, and Molt are synchronized.
"""

import os
import json
import time
import asyncio
from typing import Dict, Any, List, Optional
from platform_adapter import PlatformAdapter
from fractal_mesh import FractalMesh

class FractalRelay:
    def __init__(self):
        self.adapter = PlatformAdapter()
        self.relay_path = "/storage/emulated/0/RootBase/data/motherbrain/relay"
        self.registry_file = f"{self.relay_path}/registry.json"
        self.registry = self._load_registry()
        
        # Initialize Mesh for cross-device sync
        self.mesh = FractalMesh()
        self.mesh.on_message_received = self._handle_mesh_message

    def _load_registry(self) -> Dict[str, Any]:
        """Loads the map of all hardlined subsystems."""
        if os.path.exists(self.registry_file):
            with open(self.registry_file, 'r') as f:
                return json.load(f)
        return {
            "subsystems": {
                "CodeCity": {"status": "offline", "endpoint": "labs/Code-City-Claude", "type": "visualizer"},
                "VerticalAI": {"status": "offline", "endpoint": "labs/vertical_ai", "type": "analytics"},
                "aFiREfly": {"status": "offline", "endpoint": "labs/aFIREFLY", "type": "scout"},
                "MoltEngine": {"status": "offline", "endpoint": "molt_engine/src/core/molt.py", "type": "optimizer"},
                "KimiMentor": {"status": "offline", "endpoint": "labs/Kimi-CodeMentor-MVP", "type": "mentor"}
            },
            "last_sync": None
        }

    def _save_registry(self):
        with open(self.registry_file, 'w') as f:
            json.dump(self.registry, f, indent=4)

    def _handle_mesh_message(self, data: Dict[str, Any]):
        """
        Handles incoming messages from the Fractal Mesh.
        """
        intent = data.get("intent")
        payload = data.get("data")
        
        if intent == "BUZZ":
            print(f"[*] MESH BUZZ RECEIVED: {payload}")
            # Trigger local buzz logic
            self._log_event(f"MESH_BUZZ: {payload}")
        elif intent == "STATE_SYNC":
            print(f"[*] MESH STATE SYNC: Updating registry from {data.get('sender')}")
            self.registry["subsystems"] = payload
            self._save_registry()

    async def buzz(self, directive: str):
        """
        The 'Buzz' command: Broadcasts a directive to ALL nodes in the mesh 
        and all local subsystems.
        """
        print(f"[*] RELAY BUZZ: {directive}")
        
        # 1. Local Broadcast
        for name, info in self.registry["subsystems"].items():
            self._log_event(f"BUZZ_SENT: {name} | Directive: {directive}")
        
        # 2. Mesh Broadcast
        await self.mesh.broadcast({
            "sender": "MotherBrain_Core",
            "intent": "BUZZ",
            "data": directive
        })

    def _log_event(self, event: str):
        log_path = f"{self.relay_path}/relay_log.jsonl"
        with open(log_path, 'a') as f:
            entry = {"timestamp": time.time(), "event": event}
            f.write(json.dumps(entry) + "\n")

    def heart_beat(self):
        """
        Checks the pulse of all subsystems.
        """
        print("[*] Performing CNS Heart-Beat...")
        for name, info in self.registry["subsystems"].items():
            exists = os.path.exists(info["endpoint"])
            self.registry["subsystems"][name]["status"] = "online" if exists else "offline"
            print(f"  {name}: {self.registry['subsystems'][name]['status']}")
        
        self.registry["last_sync"] = time.time()
        self._save_registry()

if __name__ == "__main__":
    relay = FractalRelay()
    relay.heart_beat()
    relay.buzz("SYSTEM_WAKEUP")
