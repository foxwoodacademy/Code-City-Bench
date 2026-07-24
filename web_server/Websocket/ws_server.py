#!/usr/bin/env python3
# Author: BleakNarratives / Claude
# File: ws_server.py
# Path: /storage/ED7B-AD5A/root_2026/Vertical-AI/vertical-ai-unified/scripts/ws_server.py
#
# WebSocket bridge — equinex frontend <-> boardroom_orchestrator backend
# Run: python ws_server.py
# Connect: ws://localhost:8765
#
# Message format IN:  {"type": "run", "topic": "your topic here"}
# Message format OUT: {"type": "round", "round": 1, "speaker": "CHAIRMAN", "content": "..."}
#                     {"type": "round", "round": 2, "speaker": "ADVERSARY", "content": "..."}
#                     {"type": "round", "round": 3, "speaker": "ARCHITECT", "content": "..."}
#                     {"type": "directive", "content": "..."}
#                     {"type": "status", "message": "..."}
#                     {"type": "error", "message": "..."}

import asyncio
import json
import sys
import os
import requests

# ── make sure our siblings are importable ────────────────────────────────────
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import loom_reader
import mnemonic_core

# ── config ───────────────────────────────────────────────────────────────────
WS_HOST = "0.0.0.0"
WS_PORT = 8765
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:1.5b"

# ── ollama call (blocking — runs in thread pool) ──────────────────────────────
def call_ollama(prompt, context=""):
    payload = {
        "model": MODEL,
        "prompt": f"{context}\n\n{prompt}",
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 300
        }
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=300)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        return f"[Ollama error: {str(e)}]"

# ── boardroom logic (async-wrapped) ──────────────────────────────────────────
async def run_boardroom(topic, websocket):

    async def send(msg_type, **kwargs):
        await websocket.send(json.dumps({"type": msg_type, **kwargs}))

    await send("status", message=f"Boardroom assembling: {topic}")

    # load intel
    try:
        intel = loom_reader.get_threat_assessment()
        history = mnemonic_core.get_recent_history()
    except Exception as e:
        intel = "No threat data available."
        history = "No history available."

    await send("status", message="Intelligence loaded. Starting Round 1...")

    # personas
    chairman_ctx = f"""You are THE CHAIRMAN. Visionary, demanding, focused on shipping.
PAST DECISIONS: {history}
Push the project forward. Be bold."""

    adversary_ctx = f"""You are THE ADVERSARY. Red team skeptic.
RED TEAM INTEL: {intel}
PAST DECISIONS: {history}
Destroy the Chairman's optimism with evidence. Be ruthless."""

    architect_ctx = f"""You are THE ARCHITECT. Mediator and builder.
PAST DECISIONS: {history}
Synthesize vision and critique into a grounded technical plan with safeguards."""

    # round 1
    await send("status", message="Round 1: Chairman proposing...")
    loop = asyncio.get_event_loop()
    p1 = await loop.run_in_executor(
        None, call_ollama,
        f"Propose a bold feature for: '{topic}'. Short and visionary.",
        chairman_ctx
    )
    await send("round", round=1, speaker="CHAIRMAN", content=p1)

    # round 2
    await send("status", message="Round 2: Adversary attacking...")
    p2 = await loop.run_in_executor(
        None, call_ollama,
        f"The Chairman proposed: '{p1}'. Attack this based on intel. Be ruthless.",
        adversary_ctx
    )
    await send("round", round=2, speaker="ADVERSARY", content=p2)

    # round 3
    await send("status", message="Round 3: Architect synthesizing...")
    p3 = await loop.run_in_executor(
        None, call_ollama,
        f"Chairman wants: '{p1}'. Adversary warned: '{p2}'. Build a grounded architecture with safeguards.",
        architect_ctx
    )
    await send("round", round=3, speaker="ARCHITECT", content=p3)

    # directive
    directive = f"""# VERTICAL AI STRATEGIC DIRECTIVE
## Topic: {topic}

### Vision (Chairman)
{p1}

### Threat Assessment (Adversary)
{p2}

### Architecture & Mitigation (Architect)
{p3}

---
*Signed, The Board*
"""
    # save to file and mnemonic
    filename = f"directive_{topic.replace(' ', '_')[:50]}.md"
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(filepath, "w") as f:
        f.write(directive)
    mnemonic_core.add_decision(topic, p3)

    await send("directive", content=directive, filename=filename)
    await send("status", message=f"Complete. Directive saved: {filename}")

# ── websocket handler ─────────────────────────────────────────────────────────
async def handler(websocket):
    print(f"[WS] Client connected: {websocket.remote_address}")
    try:
        async for raw in websocket:
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                await websocket.send(json.dumps({"type": "error", "message": "Invalid JSON"}))
                continue

            if msg.get("type") == "run":
                topic = msg.get("topic", "").strip()
                if not topic:
                    await websocket.send(json.dumps({"type": "error", "message": "No topic provided"}))
                    continue
                await run_boardroom(topic, websocket)

            elif msg.get("type") == "ping":
                await websocket.send(json.dumps({"type": "pong"}))

            else:
                await websocket.send(json.dumps({"type": "error", "message": f"Unknown type: {msg.get('type')}"}))

    except Exception as e:
        print(f"[WS] Connection error: {e}")
    finally:
        print(f"[WS] Client disconnected")

# ── main ──────────────────────────────────────────────────────────────────────
async def main():
    try:
        import websockets
    except ImportError:
        print("Missing dependency. Run: pip install websockets --break-system-packages")
        sys.exit(1)

    print(f"[BOARDROOM] WebSocket server starting on ws://{WS_HOST}:{WS_PORT}")
    print(f"[BOARDROOM] Model: {MODEL}")
    print(f"[BOARDROOM] Ollama: {OLLAMA_URL}")
    print(f"[BOARDROOM] Ready. Waiting for connections...")

    async with websockets.serve(handler, WS_HOST, WS_PORT):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[BOARDROOM] Server stopped.")
