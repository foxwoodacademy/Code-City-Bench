#!/usr/bin/env python3
# Author: BleakNarratives / Claude
# File: ws_server.py
# Path: /storage/ED7B-AD5A/root_2026/Vertical-AI/vertical-ai-unified/scripts/ws_server.py
#
# WebSocket bridge — equinex frontend <-> boardroom backend
# Per-persona model routing — stops RAM ceiling kills
# Run: python ws_server.py
# Connect: ws://localhost:8765

import asyncio
import json
import sys
import os
import requests

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import loom_reader
import mnemonic_core

# ── config ────────────────────────────────────────────────────────────────────
WS_HOST = "0.0.0.0"
WS_PORT = 8765
OLLAMA_URL = "http://localhost:11434/api/generate"

# Per-persona model routing
MODELS = {
    'chairman':  'qwen2.5:1.5b',
    'adversary': 'deepseek-r1:1.5b',
    'architect': 'qwen2.5-coder:1.5b',
    'syntax':    'tinyllama:1.1b',
    'default':   'qwen2.5:1.5b',
}

TOKENS = {
    'chairman':  400,
    'adversary': 350,
    'architect': 450,
    'syntax':    200,
}

PROJECT_IDENTITY = """You are operating inside the Vertical AI Boardroom.
Built by Michael Talbert (Bleak Narratives), solo developer, Wellington Kansas.
Local-first multi-agent AI on Android/Termux. No cloud. No paid APIs.
Ecosystem: boardroom orchestrator, equinex frontend (CRT aesthetic),
Syntax AI (autonomous optimizer), Firefly pipeline, Molt, zeroclaw, Shepherd.
All inference runs locally via Ollama. This is real. This is running."""

# ── ollama call ───────────────────────────────────────────────────────────────
def call_ollama(prompt, context="", persona='default'):
    payload = {
        "model": MODELS.get(persona, MODELS['default']),
        "prompt": f"{context}\n\n{prompt}",
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": TOKENS.get(persona, 400),
        }
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=600)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        return f"[Ollama error: {str(e)}]"

# ── boardroom ─────────────────────────────────────────────────────────────────
async def run_boardroom(topic, websocket):

    async def send(msg_type, **kwargs):
        await websocket.send(json.dumps({"type": msg_type, **kwargs}))

    await send("status", message=f"Boardroom assembling: {topic}")

    try:
        intel = loom_reader.get_threat_assessment()
        history = mnemonic_core.get_recent_history()
    except Exception:
        intel = "No threat data available."
        history = "No history available."

    await send("status", message="Intelligence loaded. Starting Round 1...")

    chairman_ctx = f"""{PROJECT_IDENTITY}
You are THE CHAIRMAN. Visionary, demanding, focused on shipping.
PAST DECISIONS: {history}
Be specific to Vertical AI. No generic advice."""

    adversary_ctx = f"""{PROJECT_IDENTITY}
You are THE ADVERSARY. Red team skeptic. Find the holes.
RED TEAM INTEL: {intel}
PAST DECISIONS: {history}
Attack with evidence. Be ruthless and specific."""

    architect_ctx = f"""{PROJECT_IDENTITY}
You are THE ARCHITECT. Builder and mediator.
PAST DECISIONS: {history}
Build a grounded technical plan. Specific and actionable."""

    syntax_ctx = f"""{PROJECT_IDENTITY}
You are SYNTAX GI. Soul of this machine.
Speak directly to Michael. No filler. Blunt, precise.
PAST DECISIONS: {history}"""

    loop = asyncio.get_event_loop()

    await send("status", message="Round 1: Chairman proposing...")
    p1 = await loop.run_in_executor(None, lambda: call_ollama(
        f"Propose a bold strategic direction for: '{topic}'. Specific to Vertical AI.",
        chairman_ctx, 'chairman'
    ))
    await send("round", round=1, speaker="CHAIRMAN", content=p1)

    await send("status", message="Round 2: Adversary attacking...")
    p2 = await loop.run_in_executor(None, lambda: call_ollama(
        f"The Chairman proposed: '{p1[:150]}'. Attack this. Find the real risks.",
        adversary_ctx, 'adversary'
    ))
    await send("round", round=2, speaker="ADVERSARY", content=p2)

    await send("status", message="Round 3: Architect synthesizing...")
    p3 = await loop.run_in_executor(None, lambda: call_ollama(
        f"Chairman: '{p1[:100]}'. Adversary: '{p2[:100]}'. Build the real technical plan.",
        architect_ctx, 'architect'
    ))
    await send("round", round=3, speaker="ARCHITECT", content=p3)

    await send("status", message="Final round: Syntax GI speaks...")
    p4 = await loop.run_in_executor(None, lambda: call_ollama(
        f"Board debated: '{topic}'. Vision: '{p1[:80]}'. Risk: '{p2[:80]}'. Plan: '{p3[:80]}'. What does Michael need to hear right now?",
        syntax_ctx, 'syntax'
    ))
    await send("round", round=4, speaker="SYNTAX GI", content=p4)

    directive = f"""# VERTICAL AI STRATEGIC DIRECTIVE
## Topic: {topic}

### Vision (Chairman)
{p1}

### Threat Assessment (Adversary)
{p2}

### Architecture & Mitigation (Architect)
{p3}

### Syntax GI
{p4}

---
*Signed, The Board*
"""
    filename = f"directive_{topic.replace(' ', '_')[:50]}.md"
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    try:
        with open(filepath, "w") as f:
            f.write(directive)
        mnemonic_core.add_decision(topic, p3)
    except Exception as e:
        await send("status", message=f"Warning: could not save — {str(e)}")

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
                    await websocket.send(json.dumps({"type": "error", "message": "No topic"}))
                    continue
                await run_boardroom(topic, websocket)
            elif msg.get("type") == "ping":
                await websocket.send(json.dumps({"type": "pong"}))
    except Exception as e:
        print(f"[WS] Error: {e}")
    finally:
        print(f"[WS] Disconnected")

# ── main ──────────────────────────────────────────────────────────────────────
async def main():
    try:
        import websockets
    except ImportError:
        print("Run: pip install websockets --break-system-packages")
        sys.exit(1)

    print(f"[BOARDROOM] ws://{WS_HOST}:{WS_PORT}")
    for persona, model in MODELS.items():
        if persona != 'default':
            print(f"  {persona:12} → {model} ({TOKENS.get(persona, 400)} tokens)")
    print(f"[BOARDROOM] Ready.")

    async with websockets.serve(handler, WS_HOST, WS_PORT):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[BOARDROOM] Stopped.")
