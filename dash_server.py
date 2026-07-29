import http.server
import socketserver
from model_spar_simulator_RECOVERED import ModelSparSimulator

PORT = 8080
sim = ModelSparSimulator("OutClaw-Vanguard")

class DashHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Intercept the API call to feed the dashboard our recovered logic
        if self.path == '/api/spar':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            data = sim.execute_spar("Dashboard UI Hook Engaged")
            self.wfile.write(data.encode())
        else:
            # Serve index.html and other UI assets
            super().do_GET()

print(f"[YES-HUH] Dashboard API Bridge engaged.")
print(f"[YES-HUH] Open your browser to: http://localhost:{PORT}")
print(f"[YES-HUH] Hit CTRL+C when you are ready to push to GitHub.")

with socketserver.TCPServer(("", PORT), DashHandler) as httpd:
    httpd.serve_forever()
