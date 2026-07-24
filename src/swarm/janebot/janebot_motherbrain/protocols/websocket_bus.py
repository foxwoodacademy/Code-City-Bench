"""
WebSocket Bus - The network transport layer for the distributed swarm.
Handles WebSocket server management, agent connection mapping, and message routing.
"""

import asyncio
import json
import logging
import websockets
from typing import Dict, Any, Optional, Set
from dataclasses import asdict

from .security import SecurityManager
from ..core.message_bus import Message, MessageType

logger = logging.getLogger(__name__)

class WebSocketBus:
    """
    Asynchronous WebSocket transport for the JaneBot MotherBrain.
    Provides a network bridge between the central hub and remote agents.
    """
    
    def __init__(self, security_manager: SecurityManager, host: str = "0.0.0.0", port: int = 8765):
        self.host = host
        self.port = port
        self.security_manager = security_manager
        self._active_connections: Dict[str, websockets.WebSocketServerProtocol] = {}
        self._server: Optional[websockets.asyncio.server.Server] = None
        self._running = False
        
    async def start_server(self):
        """Starts the WebSocket server to listen for agent connections."""
        async with websockets.serve(self._connection_handler, self.host, self.port) as server:
            self._server = server
            self._running = True
            logger.info(f"WebSocketBus server started on {self.host}:{self.port}")
            await asyncio.Future()  # Run forever

    async def _connection_handler(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """
        Handles the lifecycle of an agent connection:
        Handshake -> Authentication -> Message Loop -> Cleanup.
        """
        agent_id = None
        try:
            # 1. Handshake & Authentication
            # Expect the first message to be a join request: {"type": "join", "token": "..."}
            auth_payload = await websocket.recv()
            data = json.loads(auth_payload)
            
            if data.get("type") == "join":
                token = data.get("token")
                agent_id = self.security_manager.validate_token(token)
                
                if agent_id:
                    await websocket.send(json.dumps({"status": "authorized", "agent_id": agent_id}))
                    self._active_connections[agent_id] = websocket
                    logger.info(f"Agent {agent_id} successfully connected and authenticated")
                else:
                    await websocket.send(json.dumps({"status": "unauthorized", "reason": "Invalid token"}))
                    await websocket.close(1008, "Unauthorized")
                    return
            else:
                await websocket.send(json.dumps({"status": "error", "reason": "Expected join request"}))
                await websocket.close(1003, "Unsupported Data")
                return

            # 2. Message Listener Loop
            async for message_json in websocket:
                try:
                    msg_data = json.loads(message_json)
                    # Convert dict back to Message object for core processing
                    message = Message.from_dict(msg_data)
                    
                    # Note: In full integration, this will be published to the MessageBus
                    logger.debug(f"Received message from agent {agent_id}: {message.message_type.name} on {message.topic}")
                    
                    # For now, we just log it. Integration will route this to MotherBrain's MessageBus.
                    
                except json.JSONDecodeError:
                    logger.error(f"Malformed JSON received from agent {agent_id}")
                except Exception as e:
                    logger.error(f"Error processing message from agent {agent_id}: {e}")

        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Agent {agent_id if agent_id else 'Unknown'} disconnected")
        except Exception as e:
            logger.error(f"Unexpected error in connection handler for {agent_id}: {e}")
        finally:
            if agent_id:
                self._active_connections.pop(agent_id, None)

    async def send_message(self, agent_id: str, message: Message):
        """Sends a serialized Message object to a specific remote agent."""
        websocket = self._active_connections.get(agent_id)
        if not websocket:
            logger.warning(f"Attempted to send message to offline agent: {agent_id}")
            return False
        
        try:
            await websocket.send(json.dumps(message.to_dict()))
            return True
        except Exception as e:
            logger.error(f"Failed to send message to agent {agent_id}: {e}")
            return False

    async def broadcast(self, message: Message):
        """Broadcasts a message to all currently connected agents."""
        if not self._active_connections:
            logger.debug("No active connections to broadcast to")
            return

        payload = json.dumps(message.to_dict())
        # Use asyncio.gather for concurrent transmission
        tasks = [ws.send(payload) for ws in self._active_connections.values()]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        success_count = sum(1 for r in results if not isinstance(r, Exception))
        logger.info(f"Broadcast sent to {success_count}/{len(self._active_connections)} agents")

    def get_active_agents(self) -> Set[str]:
        """Returns a set of all currently connected agent IDs."""
        return set(self._active_connections.keys())

    async def stop(self):
        """Gracefully shuts down the server and closes all connections."""
        self._running = False
        if self._server:
            self._server.close()
            await self._server.wait_closed()
        
        # Close all sockets
        for ws in self._active_connections.values():
            await ws.close()
            
        self._active_connections.clear()
        logger.info("WebSocketBus stopped")
