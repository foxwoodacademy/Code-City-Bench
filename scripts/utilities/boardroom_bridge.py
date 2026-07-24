#!/usr/bin/env python3
"""
boardroom_bridge.py
Flask server that connects the 3D boardroom HTML UI to vertical_ai.py.
Runs on http://127.0.0.1:8767

The UI calls:
  GET  /status   -> health check
  POST /convene  -> run boardroom, stream agent responses back
"""

import subprocess
import json
import os
import sys
import threading
from pathlib import Path
from flask import Flask, request, jsonify, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

VAI_DIR = Path("/storage/emulated/0/RootBase/Official-Vertical-AI-Boardroom")
VAI_SCRIPT = VAI_DIR / "vertical_ai.py"

# Map UI agent names to boardroom agent roles
AGENT_MAP = {
    "CFO":     "CFO",
    "CMO":     "CMO",
    "CRO":     "CRO",
    "MARKET":  "MARKET_ANALYST",
    "DEVIL":   "DEVIL",
    "CHAIR":   "CHAIRMAN",
}


@app.route("/status")
def status():
    return jsonify({
        "status": "online",
        "version": "1.0",
        "engine": str(VAI_SCRIPT),
        "ready": VAI_SCRIPT.exists()
    })


@app.route("/convene", methods=["POST"])
def convene():
    """
    Run a boardroom session and return the results.
    Body: { "brief": "Countryside Motors Wellington KS...", "rounds": 1, "tracks": 2 }
    """
    data = request.get_json(force=True)
    brief = data.get("brief", "").strip()
    rounds = data.get("rounds", 1)
    tracks = data.get("tracks", 2)
    iterations = data.get("iterations", 2)
    generations = data.get("generations", 1)

    if not brief:
        return jsonify({"error": "No brief provided"}), 400

    if not VAI_SCRIPT.exists():
        return jsonify({"error": f"vertical_ai.py not found at {VAI_SCRIPT}"}), 500

    # Build command
    cmd = [
        sys.executable, str(VAI_SCRIPT),
        "--text", brief,
        "--tracks", str(tracks),
        "--iterations", str(iterations),
        "--rounds", str(rounds),
        "--generations", str(generations),
        "--headless"
    ]

    env = os.environ.copy()
    env["OLLAMA_BOARDROOM_MODEL"] = env.get("OLLAMA_BOARDROOM_MODEL", "llama3.2:1b")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
            cwd=str(VAI_DIR),
            env=env
        )

        output = result.stdout
        stderr = result.stderr

        # Try to find the JSON output file from the run
        import glob
        json_files = sorted(
            glob.glob(str(VAI_DIR / "vai_output_*.json")),
            key=os.path.getmtime,
            reverse=True
        )

        champion = {}
        boardroom = {"debate": [], "synthesis": {}}
        session_id = ""

        if json_files:
            try:
                with open(json_files[0]) as f:
                    vai_data = json.load(f)
                champion = vai_data.get("champion", {})
                session_id = vai_data.get("session_id", "")
                br = vai_data.get("boardroom", {})
                # Normalize agent names to match the UI's AGENTS array
                name_fix = {"MARKET_ANALYST": "ANALYST", "MARKET ANALYST": "ANALYST"}
                debate = br.get("debate", [])
                for turn in debate:
                    a = turn.get("agent", "")
                    if a in name_fix:
                        turn["agent"] = name_fix[a]
                # Pass through the debate exactly as the UI expects (entry.argument)
                boardroom = {
                    "debate": debate,
                    "synthesis": br.get("synthesis", {})
                }
            except Exception as e:
                pass

        return jsonify({
            "status": "complete",
            "session_id": session_id,
            "boardroom": boardroom,
            "champion": champion,
            "raw_output": output[:2000] if output else "",
            "error": stderr[:500] if stderr and result.returncode != 0 else ""
        })

    except subprocess.TimeoutExpired:
        return jsonify({"error": "Boardroom session timed out (5 min limit)"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/quick", methods=["POST"])
def quick():
    """
    Quick single-agent response for one-on-one mode without running full boardroom.
    Body: { "agent": "CFO", "brief": "...", "history": [...] }
    """
    data = request.get_json(force=True)
    agent = data.get("agent", "advisor")
    brief = data.get("brief", "")
    history = data.get("history", [])

    # Use Ollama for quick responses
    try:
        import requests as req
        ollama_host = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
        model = os.environ.get("OLLAMA_FAST_MODEL", "llama3.2:1b")

        system = f"""You are the {agent} in a high-stakes business strategy boardroom.
Be direct, opinionated, and speak in short punchy sentences.
No corporate jargon. No bullet points. Just raw strategic thinking.
You're analyzing this business: {brief}"""

        messages = history[-4:] if history else []
        prompt = "\n".join([
            f"{'User' if m['role']=='user' else agent}: {m['content']}"
            for m in messages
        ])
        if prompt:
            prompt += f"\n{agent}:"

        resp = req.post(
            f"{ollama_host}/api/generate",
            json={
                "model": model,
                "prompt": system + "\n\n" + prompt if prompt else system + "\n\nIntroduce yourself briefly.",
                "stream": False,
                "options": {"temperature": 0.8, "num_predict": 200}
            },
            timeout=60
        )
        resp.raise_for_status()
        text = resp.json().get("response", "").strip()
        return jsonify({"text": text, "agent": agent})

    except Exception as e:
        return jsonify({"text": f"[{agent} offline: {e}]", "agent": agent})


if __name__ == "__main__":
    print("=" * 50)
    print("  BOARDROOM BRIDGE")
    print(f"  http://127.0.0.1:8767")
    print(f"  Engine: {VAI_SCRIPT}")
    print(f"  Ready: {VAI_SCRIPT.exists()}")
    print("=" * 50)
    app.run(host="127.0.0.1", port=8767, debug=False)
