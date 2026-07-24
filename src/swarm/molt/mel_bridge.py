import os
from flask import Flask, render_template_string, jsonify
import requests
import json

app = Flask(__name__)

# --- Configuration ---
# In a real setup, this would be a Nostr relay URL
RELAY_URL = os.getenv("NOSTR_RELAY", "wss://relay.damus.io") 
PRIMARY_PUBKEY = os.getenv("PRIMARY_PUBKEY", "rootbase_primary_pk")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Mel's RootBase Dashboard</title>
    <style>
        body { font-family: 'Courier New', monospace; background: #0f0f0f; color: #00ff00; padding: 20px; }
        .container { max-width: 800px; margin: auto; }
        .log-entry { margin-bottom: 20px; border-left: 2px solid #333; padding-left: 10px; }
        .thought { color: #666; font-style: italic; font-size: 0.85em; margin-bottom: 5px; display: block; }
        .output { color: #fff; font-size: 1.1em; font-weight: bold; }
        .nav-breadcrumb { background: #222; padding: 10px; border-radius: 5px; margin-bottom: 20px; color: #aaa; }
        .btn { background: #00ff00; color: #000; padding: 10px 20px; border: none; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 RootBase Navigator</h1>
        <div class="nav-breadcrumb" id="nav">Loading location...</div>
        <div id="logs"></div>
        <hr>
        <button class="btn" onclick="sendCommand('approve')">✅ Approve Move</button>
        <button class="btn" style="background: #ff0000;" onclick="sendCommand('halt')">🛑 Stop All</button>
    </div>

    <script>
        async function updateLogs() {
            const res = await fetch('/api/logs');
            const data = await res.json();
            const logDiv = document.getElementById('logs');
            logDiv.innerHTML = '';
            
            data.logs.forEach(log => {
                const div = document.createElement('div');
                div.className = 'log-entry';
                
                // Separate Thought from Output
                let content = log.text;
                if (content.includes('<thought>')) {
                    const parts = content.split('</thought>');
                    const thought = parts[0].replace('<thought>', '').trim();
                    const output = parts[1] ? parts[1].trim() : '';
                    div.innerHTML = `<span class="thought">💭 ${thought}</span><span class="output">${output}</span>`;
                } else {
                    div.innerHTML = `<span class="output">${content}</span>`;
                }
                logDiv.appendChild(div);
            });
            
            document.getElementById('nav').innerText = data.location;
        }

        async function sendCommand(cmd) {
            await fetch('/api/command', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({command: cmd})
            });
            alert('Command sent to RootBase!');
        }

        setInterval(() => {
            updateLogs();
            updateSigil();
        }, 3000);
        updateLogs();
        updateSigil();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/logs')
def get_logs():
    # Return the real session logs captured from the Nostr relay
    return jsonify({
        "location": "ModMind Pulse -> Live Stream",
        "logs": session_logs
    })

@app.route('/api/command', methods=['POST'])
def handle_command():
    cmd = request.json.get('command')
    print(f"[BRIDGE] Command received: {cmd}")
    # Here we would push a Nostr event to the primary device
    return jsonify({"status": "sent"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
 we would push a Nostr event to the primary device
    return jsonify({"status": "sent"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
  return jsonify({"status": "sent"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
