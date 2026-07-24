#!/usr/bin/env python3
"""
CodeMentor-CityBridge
Minimal HTTP bridge between VS Code extension and Code City visualizer
No WebSocket, no async—just POST/GET for Termux stability
"""
import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

# Paths relative to bridge location
MENTOR_ROOT = os.path.abspath("../CodeMentor-MVP")
CITY_ROOT = os.path.abspath("../Code-City-Claude/Code-City-Claude")

class BridgeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self._respond(200, {"status": "bridge alive", "mentor": MENTOR_ROOT, "city": CITY_ROOT})
        elif self.path == "/city/state":
            # Return last known city state (read from file)
            state_file = os.path.join(CITY_ROOT, "Code_City/code_city/data/city_data.json")
            if os.path.exists(state_file):
                with open(state_file) as f:
                    self._respond(200, json.load(f))
            else:
                self._respond(404, {"error": "no city state found"})
        else:
            self._respond(404, {"error": "unknown endpoint"})
    
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len)
        
        if self.path == "/mentor/explain":
            # Receive code explanation request from VS Code extension
            data = json.loads(body)
            # Forward to city's scanner for "monster" generation
            self._forward_to_city(data)
            self._respond(200, {"status": "explanation queued for city visualization"})
        elif self.path == "/city/attack":
            # Receive city damage report, log to mentor
            data = json.loads(body)
            self._log_to_mentor(data)
            self._respond(200, {"status": "damage logged to mentor"})
        else:
            self._respond(404, {"error": "unknown endpoint"})
    
    def _respond(self, code, data):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def _forward_to_city(self, data):
        # Write to a queue file that city scanner watches
        queue = os.path.join(CITY_ROOT, "Code_City/code_city/data/mentor_queue.jsonl")
        with open(queue, 'a') as f:
            f.write(json.dumps(data) + "\n")
    
    def _log_to_mentor(self, data):
        # Append to mentor's log
        log = os.path.join(MENTOR_ROOT, "cache/city_damage.log")
        os.makedirs(os.path.dirname(log), exist_ok=True)
        with open(log, 'a') as f:
            f.write(json.dumps(data) + "\n")
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def main():
    port = int(os.getenv("BRIDGE_PORT", "8766"))
    server = HTTPServer(("127.0.0.1", port), BridgeHandler)
    print(f"Bridge running on http://127.0.0.1:{port}")
    print(f"  Mentor: {MENTOR_ROOT}")
    print(f"  City:   {CITY_ROOT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nBridge stopped.")

if __name__ == "__main__":
    main()
