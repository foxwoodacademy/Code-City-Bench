import pytest
import asyncio
import json
import websockets
from src.janebot_motherbrain.protocols.security import SecurityManager, ValidationSchema
from src.janebot_motherbrain.protocols.websocket_bus import WebSocketBus
from src.janebot_motherbrain.core.message_bus import Message, MessageType

@pytest.mark.asyncio
async def test_security_manager_tokens():
    """Verify token generation and validation logic."""
    sm = SecurityManager()
    agent_id = "test-agent-01"
    token = sm.generate_token(agent_id)
    
    # Valid token
    assert sm.validate_token(token) == agent_id
    
    # Invalid token
    assert sm.validate_token("invalid-token") is None
    
    # Token rotation
    sm.rotate_tokens()
    assert sm.validate_token(token) is None

@pytest.mark.asyncio
async def test_security_manager_payload_validation():
    """Verify strict payload validation to prevent injection/crashes."""
    sm = SecurityManager()
    schema = ValidationSchema(fields={"task_id": str, "priority": int})
    
    # Valid payload
    assert sm.validate_payload({"task_id": "t-1", "priority": 5}, schema) is True
    
    # Missing field
    assert sm.validate_payload({"priority": 5}, schema) is False
    
    # Type mismatch
    assert sm.validate_payload({"task_id": "t-1", "priority": "high"}, schema) is False
    
    # Not a dict
    assert sm.validate_payload(["not", "a", "dict"], schema) is False

@pytest.mark.asyncio
async def test_websocket_bus_connection_and_auth():
    """Verify the full handshake: Connect -> Join -> Authorize."""
    sm = SecurityManager()
    agent_id = "auth-agent"
    token = sm.generate_token(agent_id)
    
    # Use port 0 to let OS pick an available port
    bus = WebSocketBus(security_manager=sm, host="127.0.0.1", port=0)
    
    # Start server in background
    server_task = asyncio.create_task(bus.start_server())
    # Give server a moment to start and get the assigned port
    await asyncio.sleep(0.1)
    
    # Note: In a real scenario, we'd capture the actual port. 
    # Since WebSocketBus doesn't currently expose the bound port, 
    # for this test we'll modify WebSocketBus or use a fixed test port.
    # I'll assume port 8765 for now, or implement a way to get the port.
    
    # Let's use 8765 for this specific test instance
    bus.port = 8765
    async with websockets.serve(bus._connection_handler, "127.0.0.1", 8765):
        async with websockets.connect("ws://127.0.0.1:8765") as ws:
            # 1. Send Join Request
            await ws.send(json.dumps({"type": "join", "token": token}))
            
            # 2. Verify Response
            response = json.loads(await ws.recv())
            assert response["status"] == "authorized"
            assert response["agent_id"] == agent_id
            
    server_task.cancel()

@pytest.mark.asyncio
async def test_websocket_bus_broadcast():
    """Verify that messages are correctly broadcast to all connected agents."""
    sm = SecurityManager()
    bus = WebSocketBus(security_manager=sm, host="127.0.0.1", port=8765)
    
    # Tokens for two agents
    t1 = sm.generate_token("agent-1")
    t2 = sm.generate_token("agent-2")
    
    async with websockets.serve(bus._connection_handler, "127.0.0.1", 8765):
        async with websockets.connect("ws://127.0.0.1:8765") as ws1:
            async with websockets.connect("ws://127.0.0.1:8765") as ws2:
                # Authenticate both
                await ws1.send(json.dumps({"type": "join", "token": t1}))
                await ws1.recv()
                await ws2.send(json.dumps({"type": "join", "token": t2}))
                await ws2.recv()
                
                # Prepare broadcast message
                msg = Message(
                    sender="motherbrain",
                    topic="swarm.alert",
                    message_type=MessageType.BROADCAST,
                    payload={"alert": "System Update"}
                )
                
                await bus.broadcast(msg)
                
                # Verify both received it
                resp1 = json.loads(await ws1.recv())
                resp2 = json.loads(await ws2.recv())
                
                assert resp1["topic"] == "swarm.alert"
                assert resp2["topic"] == "swarm.alert"
                assert resp1["payload"]["alert"] == "System Update"

@pytest.mark.asyncio
async def test_websocket_bus_direct_message():
    """Verify targeted delivery to a specific agent."""
    sm = SecurityManager()
    bus = WebSocketBus(security_manager=sm, host="127.0.0.1", port=8765)
    
    t1 = sm.generate_token("agent-1")
    t2 = sm.generate_token("agent-2")
    
    async with websockets.serve(bus._connection_handler, "127.0.0.1", 8765):
        async with websockets.connect("ws://127.0.0.1:8765") as ws1:
            async with websockets.connect("ws://127.0.0.1:8765") as ws2:
                # Authenticate both
                await ws1.send(json.dumps({"type": "join", "token": t1}))
                await ws1.recv()
                await ws2.send(json.dumps({"type": "join", "token": t2}))
                await ws2.recv()
                
                # Send direct to agent-2
                msg = Message(
                    sender="motherbrain",
                    recipient="agent-2",
                    topic="private.task",
                    message_type=MessageType.TASK,
                    payload={"secret": "data"}
                )
                
                await bus.send_message("agent-2", msg)
                
                # Agent 2 should receive it
                resp2 = json.loads(await ws2.recv())
                assert resp2["recipient"] == "agent-2"
                assert resp2["payload"]["secret"] == "data"
                
                # Agent 1 should NOT receive it (timeout check)
                try:
                    await asyncio.wait_for(ws1.recv(), timeout=0.1)
                    pytest.fail("Agent 1 received a message meant for Agent 2")
                except asyncio.TimeoutError:
                    pass
