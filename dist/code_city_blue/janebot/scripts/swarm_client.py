"""
Swarm Client - A standalone verification tool to test the WebSocket transport layer.
This client simulates a remote agent 'phoning home' to the MotherBrain Hub.
"""

import asyncio
import json
import logging
import websockets
from typing import Optional

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SwarmClient")

async def run_client(hub_url: str, token: str, agent_id: str):
    """Simulates an agent connection lifecycle."""
    try:
        async with websockets.connect(hub_url) as websocket:
            # 1. Authentication Handshake
            logger.info(f"Attempting to join swarm as {agent_id}...")
            join_request = {"type": "join", "token": token}
            await websocket.send(json.dumps(join_request))
            
            response = await websocket.recv()
            auth_data = json.loads(response)
            
            if auth_data.get("status") == "authorized":
                logger.info(f"Authorized! Connected as {auth_data.get('agent_id')}")
            else:
                logger.error(f"Authorization failed: {auth_data.get('reason')}")
                return

            # 2. Send a Heartbeat
            logger.info("Sending heartbeat...")
            heartbeat = {
                "message_id": "hb-123",
                "message_type": "HEARTBEAT",
                "sender": agent_id,
                "topic": "system.heartbeat",
                "payload": {"status": "online", "load": 0.1},
                "timestamp": 1621000000.0 # Dummy timestamp
            }
            await websocket.send(json.dumps(heartbeat))
            logger.info("Heartbeat sent")

            # 3. Listen for broadcasts for a while
            logger.info("Listening for broadcasts (5 seconds)...")
            try:
                # Use wait_for to avoid hanging forever
                msg = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                logger.info(f"Received message from hub: {msg}")
            except asyncio.TimeoutError:
                logger.info("No broadcasts received during window.")

    except Exception as e:
        logger.error(f"Connection error: {e}")

async def main():
    # Configuration
    HUB_URL = "ws://localhost:8765"
    TOKEN = "valid-token-placeholder" # This should be provided by the hub
    AGENT_ID = "test-agent-01"
    
    logger.info(f"Starting swarm client. Target: {HUB_URL}")
    await run_client(HUB_URL, TOKEN, AGENT_ID)

if __name__ == "__main__":
    asyncio.run(main())
