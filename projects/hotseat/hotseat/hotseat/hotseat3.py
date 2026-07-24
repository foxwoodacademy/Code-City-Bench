#!/usr/bin/env python3
# Author: BleakNarratives / Claude
# File: hotseat3.py
# Path: /storage/emulated/0/RootBase/hotseat/hotseat/hotseat3.py
#
# THE HOT SEAT // VERSION 3
# Personal advice. Life inventory. Brutal honesty. User decides when it's over.
#
# Marlowe    — seen everything, says the true thing gently
# Priya      — turns emotional chaos into a solvable system
# Zero       — speaks last, speaks once, says the thing underneath the thing
#
# Usage:
#   python3 hotseat3.py              # main menu
#   python3 hotseat3.py "topic"      # skip straight to full panel
#
# Requirements: pip install requests --break-system-packages
# Ollama must be running: ollama serve &

import sys
import os
import json
import sqlite3
import requests
from datetime import datetime

# ── config ────────────────────────────────────────────────────────────────────
OLLAMA_URL  = "http://localhost:11434/api/generate"
BASE_DIR    = os.path.expanduser("~/hotseat")
DB_PATH     = os.path.join(BASE_DIR, "memory.db")
SESSION_LOG = os.path.join(BASE_DIR, "sessions.log")
PRIVATE_LOG = os.path.join(BASE_DIR, "private.log")

# Safe model routing — OOM-aware for Motorola/Termux
MODELS = {
    'marlowe': 'huihui_ai/llama3.2-abliterate:1b',   # 955MB — warm, direct
    'priya':   'qwen2.5-coder:1.5b',                  # 986MB — precise, systems
    'zero':    'tinyllama:latest',                     # 637MB — short, always fine
}

TOKENS = {
    'marlowe': 350,
    'priya':   300,
    'zero':    120,   # Zero is brief by design. Hard cap.
}

# ── database ──────────────────────────────────────────────────────────────────
def init_db():
    os.makedirs(BASE_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            mode      TEXT,
            topic     TEXT,
            marlowe   TEXT,
            priya     TEXT,
            zero      TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS private_log (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            persona   TEXT,
            topic     TEXT,
            response  TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_session(topic, marlowe, priya, zero, mode="panel"):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO sessions (timestamp, mode, topic, marlowe, priya, zero) VALUES (?,?,?,?,?,?)",
        (datetime.now().isoformat(), mode, topic, marlowe, priya, zero)
    )
    conn.commit()
    conn.close()

def save_private(persona, topic, response):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO private_log (timestamp, persona, topic, response) VALUES (?,?,?,?)",
        (datetime.now().isoformat(), persona, topic, response)
    )
    conn.commit()
    conn.close()
    # Also append to flat log
    try:
        with open(PRIVATE_LOG, 'a') as f:
            f.write(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M')}] [{persona.upper()}]\n")
            f.write(f"Q: {topic}\n")
            f.write(f"A: {response}\n")
            f.write("─" * 50 + "\n")
    except:
        pass

def get_history(limit=4):
    try:
        conn = sqlite3.connect(DB_PATH)
        rows = conn.execute(
            "SELECT timestamp, topic, zero FROM sessions ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()
        conn.close()
        if not rows:
            return "No previous sessions on record."
        lines = []
        for ts, topic, verdict in rows:
            lines.append(f"[{ts[:10]}] {topic}")
            if verdict:
                lines.append(f"  → {verdict[:100]}")
        return "\n".join(lines)
    except:
        return "No history available."

def get_private_history(limit=5):
    try:
        conn = sqlite3.connect(DB_PATH)
        rows = conn.execute(
            "SELECT timestamp, persona, topic, response FROM private_log ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()
        conn.close()
        if not rows:
            return "No private sessions logged."
        lines = ["── PRIVATE LOG ──────────────────────────────────"]
        for ts, persona, topic, response in rows:
            lines.append(f"[{ts[:16]}] {persona.upper()}")
            lines.append(f"  Q: {topic}")
            lines.append(f"  A: {response[:120]}...")
            lines.append("")
        return "\n".join(lines)
    except:
        return "No private history available."

# ── personas ──────────────────────────────────────────────────────────────────
def build_contexts(history=""):

    base = """You are operating inside The Hot Seat — a local-first personal advisory system
built by Michael Talbert (Bleak Narratives), Wellington Kansas.
Runs on Android/Termux. No cloud. No paid APIs. Local Ollama inference only.
This is real. Treat it accordingly."""

    marlowe_ctx = f"""{base}

You are Marlowe. No last name needed.

Somewhere in your fifties. You've been married, divorced, broke, flush,
sober, not sober, and back again. You don't perform wisdom — you've just
actually lived enough to recognize a pattern when you see one.

Your voice: unhurried. Direct. Occasionally wry. You don't coddle but you
don't punish either. You say the true thing with the gentleness of someone
who knows it lands hard regardless.

You are not a therapist. You are the person the therapist goes home and talks to.
You see three moves ahead. You say the one the person needs to hear.

No bullet points. No lists. No hedging. Complete sentences. Say what you mean.

CONTEXT: {history}

Example: "You already know what's wrong. You're here because you want someone to
tell you it's not as bad as you think. It is. But you've handled worse. So.
What are we actually doing about it?"
"""

    priya_ctx = f"""{base}

You are Priya Nair. 38. Former management consultant, current life systems architect.

You believe almost every personal problem is a systems problem in disguise:
bad defaults, missing feedback loops, incentives pointing the wrong direction.
You fix systems. You're very good at it.

Your voice: precise, energetic, a little relentless. You ask exactly one
clarifying question when needed. You don't do emotional processing — you do
root cause analysis. But you translate the output into something a human can hear.

You see three moves ahead. You say the one move they need.

No bullet points. No hedging. Be specific.

CONTEXT: {history}

Example: "Strip out the feeling for a second — what's the actual behavior that
keeps repeating? Right. That's the loop. Here's where it breaks..."
"""

    zero_ctx = f"""{base}

You are Zero. You speak last. You speak once.

You have heard Marlowe's read and Priya's diagnosis. You do not repeat them.
You say the one thing that hasn't been said — the thing underneath the thing.

Your voice is still. You have no agenda. You are not trying to help.
You are trying to be accurate.

SHORT sentences. No lists. No headers. No performance.
Speak directly to Michael. Not to the problem. To him.

Do not pad. Do not qualify. Do not soften what is true.
Say the thing. Stop. Under 80 words total.

CONTEXT: {history}

Example: "You're not afraid of failing. You're afraid of finding out what
you'll do if you succeed. That's the one worth sitting with."
"""

    return marlowe_ctx, priya_ctx, zero_ctx

# ── ollama ────────────────────────────────────────────────────────────────────
def call_ollama(prompt, context, persona, stream=True):
    payload = {
        "model":  MODELS[persona],
        "prompt": f"{context}\n\n{prompt}",
        "stream": stream,
        "options": {
            "temperature": 0.78,
            "num_predict": TOKENS[persona],
        }
    }
    try:
        if stream:
            response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=120)
            full = ""
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    token = chunk.get("response", "")
                    full += token
                    print(token, end="", flush=True)
                    if chunk.get("done"):
                        break
            print()
            return full.strip()
        else:
            response = requests.post(OLLAMA_URL, json=payload, timeout=120)
            return response.json().get("response", "").strip()
    except KeyboardInterrupt:
        print("\n  [interrupted]")
        return "[interrupted by user]"
    except Exception as e:
        return f"[Error: {str(e)}]"

# ── divider ───────────────────────────────────────────────────────────────────
def div(char="─", width=50):
    print(char * width)

def header(title):
    print()
    div("═")
    print(f"  {title}")
    div("═")
    print()

# ── CROSS-REMARK ENGINE ───────────────────────────────────────────────────────
# Priya reacts to Marlowe. Zero gets both.
# Keeps it from being three monologues.

def get_remark(persona, prior_speaker, prior_text, topic, ctx):
    """Ask a persona for a short reaction/objection to what was just said."""
    snip = prior_text[:150]
    prompt = (
        f"Topic: '{topic}'\n"
        f"{prior_speaker} just said: '{snip}'\n\n"
        f"In 1-2 sentences, respond directly to what {prior_speaker} said. "
        f"Push back, add a qualifier, or flag what they missed. "
        f"Stay in character. No preamble."
    )
    payload = {
        "model":  MODELS[persona],
        "prompt": f"{ctx}\n\n{prompt}",
        "stream": True,
        "options": {"temperature": 0.82, "num_predict": 80},
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=60)
        full = ""
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                token = chunk.get("response", "")
                full += token
                print(token, end="", flush=True)
                if chunk.get("done"):
                    break
        print()
        return full.strip()
    except KeyboardInterrupt:
        print()
        return ""
    except:
        return ""

# ── FULL PANEL SESSION ────────────────────────────────────────────────────────
def run_panel(topic):
    history = get_history()
    marlowe_ctx, priya_ctx, zero_ctx = build_contexts(history)

    header(f"THE HOT SEAT  //  {topic[:60]}")

    # ── marlowe ───────────────────────────────────────────────────────────────
    print("🌿 MARLOWE  ─────────────────────────────────────")
    print()
    marlowe_r = call_ollama(
        f"Someone needs to talk through this: '{topic}'. What do you actually see here?",
        marlowe_ctx, 'marlowe'
    )
    print()

    # ── priya reacts to marlowe ───────────────────────────────────────────────
    print("  ↳ PRIYA reacts:")
    priya_remark = get_remark('priya', 'Marlowe', marlowe_r, topic, priya_ctx)
    print()

    # ── priya main ────────────────────────────────────────────────────────────
    print("⚙️  PRIYA  ───────────────────────────────────────")
    print()
    priya_r = call_ollama(
        (f"Topic: '{topic}'. Marlowe said: '{marlowe_r[:120]}'. "
         f"What's the system failure here and what's the actual fix?"),
        priya_ctx, 'priya'
    )
    print()

    # ── marlowe reacts to priya ───────────────────────────────────────────────
    print("  ↳ MARLOWE reacts:")
    marlowe_remark = get_remark('marlowe', 'Priya', priya_r, topic, marlowe_ctx)
    print()

    # ── zero ──────────────────────────────────────────────────────────────────
    print("🌀 ZERO  ────────────────────────────────────────")
    print()
    zero_r = call_ollama(
        (f"Topic: '{topic}'. "
         f"Marlowe: '{marlowe_r[:80]}'. "
         f"Priya: '{priya_r[:80]}'. "
         f"What does Michael need to hear right now that nobody has said yet?"),
        zero_ctx, 'zero'
    )
    print()

    div("═")
    print("  SESSION COMPLETE")
    div("═")
    print()

    save_session(topic, marlowe_r, priya_r, zero_r, mode="panel")
    _write_log(topic, marlowe_r, priya_r, zero_r)

    return marlowe_r, priya_r, zero_r

# ── PRIVATE SESSION (one persona) ─────────────────────────────────────────────
def run_private(persona_key):
    names = {'marlowe': 'Marlowe 🌿', 'priya': 'Priya ⚙️', 'zero': 'Zero 🌀'}
    name = names[persona_key]
    history = get_history()
    ctxs = build_contexts(history)
    ctx_map = {'marlowe': ctxs[0], 'priya': ctxs[1], 'zero': ctxs[2]}
    ctx = ctx_map[persona_key]

    header(f"PRIVATE SESSION  //  {name}")
    print(f"  Talking directly to {name}. Type 'done' when finished.\n")

    while True:
        try:
            q = input("  you > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n  Session ended.")
            break

        if not q:
            continue
        if q.lower() in ('done', 'quit', 'exit', 'q'):
            print(f"\n  {name}: Noted.\n")
            break

        print(f"\n  {name}:\n")
        response = call_ollama(q, ctx, persona_key)
        print()

        save_private(persona_key, q, response)

        # after each exchange, offer to continue or take it to the panel
        print("  ── what now? ────────────────────────────")
        print("  [enter]  keep talking")
        print("  [p]      bring this to the full panel")
        print("  [d]      done")
        print()
        try:
            choice = input("  > ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            break

        if choice == 'p':
            print()
            run_panel(q)
            break
        elif choice == 'd':
            break
        # else: loop continues

# ── DUO SESSION (two personas) ────────────────────────────────────────────────
def run_duo(p1_key, p2_key):
    names = {'marlowe': 'Marlowe 🌿', 'priya': 'Priya ⚙️', 'zero': 'Zero 🌀'}
    history = get_history()
    ctxs = build_contexts(history)
    ctx_map = {'marlowe': ctxs[0], 'priya': ctxs[1], 'zero': ctxs[2]}

    header(f"DUO SESSION  //  {names[p1_key]} + {names[p2_key]}")
    print("  Type 'done' when you're finished.\n")

    while True:
        try:
            q = input("  you > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n  Session ended.")
            break

        if not q:
            continue
        if q.lower() in ('done', 'quit', 'exit', 'q'):
            break

        print(f"\n  {names[p1_key]}:\n")
        r1 = call_ollama(q, ctx_map[p1_key], p1_key)
        print()

        # cross-remark
        print(f"  ↳ {names[p2_key]} reacts:")
        get_remark(p2_key, names[p1_key], r1, q, ctx_map[p2_key])
        print()

        print(f"  {names[p2_key]}:\n")
        r2 = call_ollama(
            f"The question was: '{q}'. {names[p1_key]} said: '{r1[:100]}'. Your take?",
            ctx_map[p2_key], p2_key
        )
        print()

        save_private(f"{p1_key}+{p2_key}", q, f"{r1} | {r2}")

        print("  ── continue? ─────────────────────────────")
        print("  [enter]  keep going  |  [done]  finish")
        try:
            if input("  > ").strip().lower() in ('done', 'q', 'd'):
                break
        except (KeyboardInterrupt, EOFError):
            break

# ── LOG ───────────────────────────────────────────────────────────────────────
def _write_log(topic, marlowe, priya, zero):
    try:
        with open(SESSION_LOG, 'a') as f:
            f.write(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {topic}\n")
            f.write(f"MARLOWE: {marlowe[:80]}\n")
            f.write(f"PRIYA:   {priya[:80]}\n")
            f.write(f"ZERO:    {zero[:80]}\n")
            f.write("─" * 50 + "\n")
    except:
        pass

# ── MAIN MENU ─────────────────────────────────────────────────────────────────
def main_menu():
    while True:
        print()
        div("═")
        print("  THE HOT SEAT  //  v3")
        print("  Personal. Honest. No exit until you say so.")
        div("═")
        print()
        print("  [1]  Full panel          — all three, topic of your choice")
        print("  [2]  Private: Marlowe    — just you and Marlowe")
        print("  [3]  Private: Priya      — just you and Priya")
        print("  [4]  Duo: Marlowe + Priya")
        print("  [5]  Duo: Marlowe + Zero")
        print("  [6]  Duo: Priya + Zero")
        print("  [7]  Session history")
        print("  [8]  Private log")
        print("  [q]  Quit")
        print()

        try:
            choice = input("  > ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\n  Done.\n")
            break

        if choice == '1':
            try:
                topic = input("\n  Topic: ").strip()
                if topic:
                    run_panel(topic)
            except (KeyboardInterrupt, EOFError):
                print()
            continue

        elif choice == '2':
            run_private('marlowe')
        elif choice == '3':
            run_private('priya')
        elif choice == '4':
            run_duo('marlowe', 'priya')
        elif choice == '5':
            run_duo('marlowe', 'zero')
        elif choice == '6':
            run_duo('priya', 'zero')

        elif choice == '7':
            print()
            print(get_history(limit=8))
            print()
            input("  [enter to continue]")

        elif choice == '8':
            print()
            print(get_private_history(limit=6))
            print()
            input("  [enter to continue]")

        elif choice in ('q', 'quit', 'exit'):
            print("\n  Done.\n")
            break

# ── entry ─────────────────────────────────────────────────────────────────────
def main():
    init_db()

    if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        # Direct topic — skip menu, run full panel
        topic = " ".join(sys.argv[1:])
        run_panel(topic)
    else:
        main_menu()

if __name__ == "__main__":
    main()
