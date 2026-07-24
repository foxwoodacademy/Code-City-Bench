import http.server
import socketserver
import json
import os

PORT = 8766
MENTOR = "/storage/emulated/0/RootBase/CodeMentor-MVP"
CITY = "/storage/emulated/0/RootBase/Code-City-Claude/Code-City-Claude"

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        out = {"status": "ok", "mentor": MENTOR, "city": CITY}
        self.wfile.write(json.dumps(out).encode())

    def log_message(self, format, *args):
        pass

with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
    print("Bridge on port", PORT)
    httpd.serve_forever()
