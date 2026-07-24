#!/usr/bin/env python3
"""
MotherBrain Swarm Unified Communication Bus
Enables cross-project service discovery, standard logging, and state telemetry.
Path: /storage/emulated/0/RootBase/data/motherbrain/api/swarm_bus.py
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Optional

BUS_ROOT = Path("/storage/emulated/0/RootBase/data/motherbrain/api/bus")
REGISTRY_DIR = BUS_ROOT / "registry"
QUEUE_DIR = BUS_ROOT / "queues"

class SwarmNode:
    """Every project instantiates this handler to immediately join the ecosystem network."""
    def __init__(self, node_name: str, capabilities: List[str]):
        self.node_name = node_name.lower().strip().replace(" ", "_")
        self.capabilities = capabilities
        self.registry_file = REGISTRY_DIR / f"{self.node_name}.json"
        self.queue_file = QUEUE_DIR / f"{self.node_name}.jsonl"
        
        # Ensure underlying channel geometry exists
        REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
        QUEUE_DIR.mkdir(parents=True, exist_ok=True)
        self._heartbeat()

    def _heartbeat(self):
        """Registers or updates the engine's active network posture."""
        manifest = {
            "node_name": self.node_name,
            "pid": os.getpid(),
            "last_seen": time.time(),
            "capabilities": self.capabilities,
            "status": "ACTIVE"
        }
        with open(self.registry_file, "w") as f:
            json.dump(manifest, f, indent=2)

    def broadcast(self, target_node: str, event_type: str, payload: Dict) -> bool:
        """Sends a standardized JSON packet to another module's input queue."""
        target = target_node.lower().strip()
        target_queue = QUEUE_DIR / f"{target}.jsonl"
        
        packet = {
            "sender": self.node_name,
            "timestamp": time.time(),
            "event": event_type.upper(),
            "payload": payload
        }
        
        try:
            with open(target_queue, "a") as f:
                f.write(json.dumps(packet) + "\n")
            return True
        except Exception:
            return False

    def read_inbound_queue(self) -> List[Dict]:
        """Consumes all unread pipeline messages waiting for this specific execution layer."""
        self._heartbeat() # Signal liveness during poll
        if not self.queue_file.exists():
            return []
            
        messages = []
        try:
            with open(self.queue_file, "r") as f:
                for line in f:
                    if line.strip():
                        messages.append(json.loads(line.strip()))
            # Clear queue file upon ingestion to prevent infinite reprocessing loops
            self.queue_file.unlink()
        except Exception:
            pass
        return messages

    def discover_network(self) -> Dict[str, Dict]:
        """Returns all other active nodes currently online in the RootBase system."""
        network = {}
        for node_manifest in REGISTRY_DIR.glob("*.json"):
            try:
                with open(node_manifest) as f:
                    data = json.load(f)
                    # If a node hasn't pinged in 1 hour, consider it stale
                    if time.time() - data.get("last_seen", 0) < 3600:
                        network[data["node_name"]] = data
            except Exception:
                continue
        return network
