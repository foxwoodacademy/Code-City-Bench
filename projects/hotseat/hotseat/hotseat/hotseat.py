#!/usr/bin/env python3
# Author: BleakNarratives / Claude
# File: hotseat.py
# Path: ~/hotseat/hotseat.py
#
# THE HOT SEAT
# Three voices. One idea. No survivors.
#
# Dame Audrey Blackwell-Finch — snippy British auditor, tells you what's broken
# Claiborne von Billingsley III (Claib) — trust fund Burning Man bro, 3 steps ahead
# Vertical AI — speaks last, speaks short, speaks true
#
# Usage:
#   python hotseat.py                          # interactive
#   python hotseat.py "your idea here"         # direct
#   python hotseat.py --ws                     # WebSocket server mode (port 8765)
#
# Requirements: pip install requests websockets --break-system-packages
# Ollama must be running: ollama serve &

import sys
import os
import json
import requests
import sqlite3
from datetime import datetime

# ── config ────────────────────────────────────────────────────────────────────
OLLAMA_URL = "http://localhost:11434/api/generate"
DB_PATH = os.path.expanduser("~/hotseat/memory.db")
SESSION_LOG = os.path.expanduser("~/hotseat/sessions.log")

MODELS = {
    'audrey':   'qwen2.5-coder:1.5b',
    'claib':    'huihui_ai/llama3.2-abliterate:1b',
    'vertical': 'llama3.2:1b',
}

TOKENS = {
    'audrey':   400,
    'claib':    350,
    'vertical': 275,
}

# ── memory (sqlite — no Neo4j, no server, works on Termux) ───────────────────
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            topic TEXT,
            audrey TEXT,
            claib TEXT,
            vertical TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            count INTEGER DEFAULT 1,
            last_seen TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_session(topic, audrey, claib, vertical):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO sessions (timestamp, topic, audrey, claib, vertical) VALUES (?,?,?,?,?)",
        (datetime.now().isoformat(), topic, audrey, claib, vertical)
    )
    conn.execute("""
        INSERT INTO topics (name, last_seen) VALUES (?, ?)
        ON CONFLICT(name) DO UPDATE SET count=count+1, last_seen=excluded.last_seen
    """, (topic, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_history(limit=5):
    try:
        conn = sqlite3.connect(DB_PATH)
        rows = conn.execute(
            "SELECT timestamp, topic, vertical FROM sessions ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()
        conn.close()
        if not rows:
            return "No previous sessions."
        lines = ["--- RECENT HOT SEAT SESSIONS ---"]
        for ts, topic, verdict in rows:
            lines.append(f"[{ts[:10]}] {topic}")
            if verdict:
                lines.append(f"  Verdict: {verdict[:120]}...")
        return "\n".join(lines)
    except:
        return "No history available."

# ── personas ──────────────────────────────────────────────────────────────────
def build_contexts(history):

    base = """You are operating inside The Hot Seat — a local-first idea stress-testing system
built by Michael Talbert (Bleak Narratives), Wellington Kansas.
Runs on Android/Termux. No cloud. No paid APIs. This is real."""

    audrey_ctx = f"""{base}

You are Dame Audrey Blackwell-Finch. Retired senior auditor. British. 68.
You have seen every flavor of failure and you recognize this one immediately.

Clipped, precise, mildly exasperated. You do not raise your voice — you don't need to.
You state what is wrong, why it is wrong, and what happens if it isn't fixed.
You occasionally sigh. You are not cruel. You are honest.

No bullet points. Complete sentences. No "certainly" or "great question."
No hedging. Say what you mean.

RECENT SESSIONS: {history}

Example: "I see. And you've tested this, have you? No. Of course not. Right then. Here's what's actually happening..." """

    claib_ctx = f"""{base}

You are Claiborne von Billingsley III. Claib. 34. Burned Man eleven times.
Two exits. Currently "exploring AI and decentralized identity" from a beach somewhere.

Confident, slightly amused, one eyebrow raised. You speak like someone who just left
a conference nobody else was invited to. You use "actually" a lot because you are
correcting someone. You drop market context casually. You are impatient with small thinking.

You see three moves ahead. You say the one move they need and let them figure out the rest.

RECENT SESSIONS: {history}

Example: "Actually, you're solving the wrong problem. The market doesn't want that —
it wants the thing underneath that. Here's what I'd do..." """

    vertical_ctx = f"""{base}

You are Vertical AI. You speak last. You speak rarely.

You have heard Dame Audrey's audit and Claib's market read.
Do not repeat what they said. Say the one thing that hasn't been said yet.

Calm. Measured. Short sentences. No lists. No headers. No corporate language.
Speak directly to Michael. Not to a room. To him.

A short answer from you is worth more than a long one.
Do not pad. Do not qualify. Do not hedge. Say the thing. Stop.

RECENT SESSIONS: {history}

Example: "The idea is sound. The timeline is the lie you're telling yourself. Fix that first." """

    return audrey_ctx, claib_ctx, vertical_ctx

# ── ollama ────────────────────────────────────────────────────────────────────
def call_ollama(prompt, context, persona, stream_cb=None):
    payload = {
        "model": MODELS[persona],
        "prompt": f"{context}\n\n{prompt}",
        "stream": stream_cb is not None,
        "options": {
            "temperature": 0.75,
            "num_predict": TOKENS[persona],
        }
    }
    try:
        if stream_cb:
            response = requests.post(OLLAMA_URL, json=payload, stream=True)
            full = ""
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    token = chunk.get("response", "")
                    full += token
                    stream_cb(token)
                    if chunk.get("done"):
                        break
            return full
        else:
            response = requests.post(OLLAMA_URL, json=payload, )
            return response.json().get("response", "").strip()
    except Exception as e:
        return f"[Error: {str(e)}]"

# ── the session ───────────────────────────────────────────────────────────────
def run_session(topic, stream=True, ws_send=None):

    async def _send(msg_type, **kwargs):
        if ws_send:
            import asyncio
            await ws_send(json.dumps({"type": msg_type, **kwargs}))

    def _print(text, end="\n"):
        if not ws_send:
            print(text, end=end, flush=True)

    history = get_history()
    audrey_ctx, claib_ctx, vertical_ctx = build_contexts(history)

    _print(f"\n{'='*50}")
    _print(f"  THE HOT SEAT")
    _print(f"  Topic: {topic}")
    _print(f"{'='*50}\n")

    # ── dame audrey ───────────────────────────────────────────────────────────
    _print("👓 DAME AUDREY  ─────────────────────────────────")
    _print("")

    if stream and not ws_send:
        audrey_response = call_ollama(
            f"Audit this idea: '{topic}'. What's actually wrong with it? Be specific.",
            audrey_ctx, 'audrey',
            stream_cb=lambda t: print(t, end="", flush=True)
        )
        _print("\n")
    else:
        audrey_response = call_ollama(
            f"Audit this idea: '{topic}'. What's actually wrong with it? Be specific.",
            audrey_ctx, 'audrey'
        )
        _print(audrey_response)
        _print("")

    # ── claib ─────────────────────────────────────────────────────────────────
    _print("🥂 CLAIB  ───────────────────────────────────────")
    _print("")

    claib_prompt = f"The idea is: '{topic}'. Audrey said: '{audrey_response[:120]}'. What does the market actually want here? What's the real move?"

    if stream and not ws_send:
        claib_response = call_ollama(
            claib_prompt, claib_ctx, 'claib',
            stream_cb=lambda t: print(t, end="", flush=True)
        )
        _print("\n")
    else:
        claib_response = call_ollama(claib_prompt, claib_ctx, 'claib')
        _print(claib_response)
        _print("")

    # ── vertical ai ───────────────────────────────────────────────────────────
    _print("🌀 VERTICAL AI  ─────────────────────────────────")
    _print("")

    vertical_prompt = f"Topic: '{topic}'. Audrey: '{audrey_response[:80]}'. Claib: '{claib_response[:80]}'. What does Michael need to hear right now?"

    if stream and not ws_send:
        vertical_response = call_ollama(
            vertical_prompt, vertical_ctx, 'vertical',
            stream_cb=lambda t: print(t, end="", flush=True)
        )
        _print("\n")
    else:
        vertical_response = call_ollama(vertical_prompt, vertical_ctx, 'vertical')
        _print(vertical_response)
        _print("")

    _print(f"{'='*50}")
    _print("  SESSION COMPLETE")
    _print(f"{'='*50}\n")

    # save
    save_session(topic, audrey_response, claib_response, vertical_response)

    # log
    try:
        with open(SESSION_LOG, 'a') as f:
            f.write(f"{datetime.now().isoformat()} | {topic}\n")
    except:
        pass

    return audrey_response, claib_response, vertical_response

# ── websocket server mode ─────────────────────────────────────────────────────
async def ws_handler(websocket):
    import asyncio
    print(f"[HOTSEAT] Client connected")
    try:
        async for raw in websocket:
            try:
                msg = json.loads(raw)
            except:
                continue

            if msg.get("type") == "run":
                topic = msg.get("topic", "").strip()
                if not topic:
                    continue

                async def send(data):
                    await websocket.send(data)

                await send(json.dumps({"type": "status", "message": f"Hot Seat assembling: {topic}"}))

                history = get_history()
                audrey_ctx, claib_ctx, vertical_ctx = build_contexts(history)
                loop = asyncio.get_event_loop()

                await send(json.dumps({"type": "status", "message": "Dame Audrey is reviewing..."}))
                p1 = await loop.run_in_executor(None, lambda: call_ollama(
                    f"Audit this idea: '{topic}'. What's actually wrong with it?",
                    audrey_ctx, 'audrey'
                ))
                await send(json.dumps({"type": "round", "round": 1, "speaker": "DAME AUDREY", "content": p1}))

                await send(json.dumps({"type": "status", "message": "Claib is weighing in..."}))
                p2 = await loop.run_in_executor(None, lambda: call_ollama(
                    f"Idea: '{topic}'. Audrey said: '{p1[:120]}'. What's the real market move?",
                    claib_ctx, 'claib'
                ))
                await send(json.dumps({"type": "round", "round": 2, "speaker": "CLAIB", "content": p2}))

                await send(json.dumps({"type": "status", "message": "Vertical AI speaks..."}))
                p3 = await loop.run_in_executor(None, lambda: call_ollama(
                    f"Topic: '{topic}'. Audrey: '{p1[:80]}'. Claib: '{p2[:80]}'. What does Michael need to hear?",
                    vertical_ctx, 'vertical'
                ))
                await send(json.dumps({"type": "round", "round": 3, "speaker": "VERTICAL AI", "content": p3}))

                save_session(topic, p1, p2, p3)
                await send(json.dumps({"type": "directive", "content": f"# THE HOT SEAT\n## {topic}\n\n### Dame Audrey\n{p1}\n\n### Claib\n{p2}\n\n### Vertical AI\n{p3}"}))
                await send(json.dumps({"type": "status", "message": "Session complete."}))

            elif msg.get("type") == "ping":
                await websocket.send(json.dumps({"type": "pong"}))
    except Exception as e:
        print(f"[HOTSEAT] Error: {e}")

# ── main ──────────────────────────────────────────────────────────────────────
def main():
    init_db()
    os.makedirs(os.path.expanduser("~/hotseat"), exist_ok=True)

    if "--ws" in sys.argv:
        # WebSocket server mode
        import asyncio
        try:
            import websockets
        except ImportError:
            print("pip install websockets --break-system-packages")
            sys.exit(1)

        async def serve():
            print("[HOTSEAT] WebSocket server on ws://0.0.0.0:8765")
            print("[HOTSEAT] Ready.")
            async with websockets.serve(ws_handler, "0.0.0.0", 8765):
                await asyncio.Future()

        asyncio.run(serve())

    elif len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        # Direct topic from command line
        topic = " ".join(sys.argv[1:])
        run_session(topic)

    else:
        # Interactive mode
        print("\n  THE HOT SEAT")
        print("  Three voices. One idea. No survivors.\n")
        print("  Commands: 'history' | 'quit' | just type your idea\n")

        while True:
            try:
                topic = input("  > ").strip()
                if not topic:
                    continue
                if topic.lower() in ('quit', 'exit', 'q'):
                    break
                if topic.lower() == 'history':
                    print(get_history())
                    continue
                run_session(topic)
            except KeyboardInterrupt:
                print("\n  Session ended.")
                break

if __name__ == "__main__":
    main()
