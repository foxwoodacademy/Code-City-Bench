# AUTHOR(S) fractal_mesh.py
"""
Fractal Mesh: The Communication Layer.
Implements a lightweight, cross-platform WebSocket relay for 
synchronizing state and broadcasting directives across the MotherBrain fractal.
"""

import asyncio
import json
import os
import socket
from typing import Dict, Any, Optional, Callable
import websockets

class FractalMesh:
    def __init__(self, host: str = "0.0.0.0", port: int = 8765):
        self.host = host
        self.port = port
        self.connections = set()
        self.is_hub = False
        self.hub_address = None
        self.on_message_received: Optional[Callable[[Dict[str, Any]], None]] = None

    async def start_hub(self):
        """
        Starts the MotherBrain as a Hub, allowing other nodes to connect.
        """
        self.is_hub = True
        print(f"[*] Starting Fractal Mesh Hub on {self.host}:{self.port}...")
        async with websockets.serve(self._handle_connection, self.host, self.port):
            await asyncio.Future()  # Run forever

    async def connect_to_hub(self, hub_ip: str):
        """
        Connects the current instance as a Node to a remote Hub.
        """
        self.hub_address = f"ws://{hub_ip}:{self.port}"
        print(f"[*] Connecting to Fractal Mesh Hub at {self.hub_address}...")
        try:
            async with websockets.connect(self.hub_address) as websocket:
                self.connections.add(websocket)
                # Listen for messages from the hub
                async for message in websocket:
                    await self._process_message(message)
        except Exception as e:
            print(f"[!] Mesh Connection Error: {e}")

    async def _handle_connection(self, websocket):
        """
        Hub-side handler for incoming node connections.
        """
        self.connections.add(websocket)
        print(f"[+] New Node joined the Mesh: {websocket.remote_address}")
        try:
            async for message in websocket:
                await self._process_message(message)
        except websockets.exceptions.ConnectionClosed:
            print(f"[-] Node left the Mesh: {websocket.remote_address}")
        finally:
            self.connections.remove(websocket)

    async def _process_message(self, message: str):
        """
        Decodes and dispatches incoming mesh messages.
        """
        try:
            data = json.loads(message)
            if self.on_message_received:
                self.on_message_received(data)
        except json.JSONDecodeError:
            print(f"[!] Received malformed mesh message: {message}")

    async def broadcast(self, payload: Dict[str, Any]):
        """
        Sends a message to all connected nodes in the mesh.
        """
        if not self.connections:
            return

        message = json.dumps(payload)
        # Use asyncio.gather to send to all nodes concurrently
        await asyncio.gather(
            *[conn.send(message) for conn in self.connections], 
            return_exceptions=True
        )

# -----------------------------------------------------------------------------
# LOWER CLASSES & HELPERS (The Boilerplate)
# -----------------------------------------------------------------------------

class MeshPacket:
    """Standard packet format for mesh communication."""
    def __init__(self, sender: str, intent: str, data: Any):
        self.packet = {
            "sender": sender,
            "intent": intent,
            "data": data,
            "timestamp": os.times().elapsed
        }

    def serialize(self) -> str:
        return json.dumps(self.packet)
