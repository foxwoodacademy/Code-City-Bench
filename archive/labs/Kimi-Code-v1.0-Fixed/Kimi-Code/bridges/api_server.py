"""
Kimi-Code: API Server & Dashboard
Lightweight HTTP server for Termux/localhost.
"""
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

class DashboardHandler(BaseHTTPRequestHandler):
    """HTTP handler for dashboard and API."""

    def __init__(self, state_engine, api_bridge, *args, **kwargs):
        self.state = state_engine
        self.api = api_bridge
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        pass  # Quiet mode

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        routes = {
            '/': self._serve_dashboard,
            '/api/status': self._api_status,
            '/api/skills': self._api_skills,
            '/api/hats': self._api_hats,
            '/api/challenge': self._api_challenge,
            '/api/progress': self._api_progress,
            '/api/skill-tree': self._api_skill_tree
        }

        handler = routes.get(path, self._serve_404)
        handler(query)

    def _serve_dashboard(self, query):
        """Serve main dashboard HTML."""
        data = self.state.get_dashboard_data()

        html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Kimi-Code Dashboard</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #0a0a1a; color: #e0e0e0; }}
.header {{ background: linear-gradient(135deg, #1a1a3e 0%, #16213e 100%); padding: 30px; text-align: center; border-bottom: 2px solid #00ff88; }}
.header h1 {{ color: #00ff88; font-size: 2.5em; margin-bottom: 10px; }}
.header p {{ color: #888; }}
.metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; padding: 30px; max-width: 1200px; margin: 0 auto; }}
.metric {{ background: #1a1a2e; border-radius: 12px; padding: 25px; text-align: center; border: 1px solid #333; transition: transform 0.2s; }}
.metric:hover {{ transform: translateY(-5px); border-color: #00ff88; }}
.metric .num {{ font-size: 3em; font-weight: bold; color: #00ff88; display: block; margin: 10px 0; }}
.metric label {{ color: #888; font-size: 0.9em; text-transform: uppercase; letter-spacing: 1px; }}
.section {{ max-width: 1200px; margin: 0 auto; padding: 0 30px 30px; }}
.section h2 {{ color: #60a5fa; margin-bottom: 20px; font-size: 1.5em; }}
.skill-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; }}
.skill-item {{ background: #1a1a2e; padding: 15px; border-radius: 8px; display: flex; align-items: center; gap: 15px; }}
.skill-bar {{ flex: 1; height: 8px; background: #333; border-radius: 4px; overflow: hidden; }}
.skill-fill {{ height: 100%; background: linear-gradient(90deg, #00ff88, #60a5fa); border-radius: 4px; transition: width 0.5s; }}
.skill-name {{ width: 120px; font-size: 0.9em; color: #ccc; }}
.skill-value {{ width: 40px; text-align: right; color: #00ff88; font-weight: bold; }}
.hats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }}
.hat-card {{ background: #1a1a2e; padding: 20px; border-radius: 10px; text-align: center; border-left: 4px solid; }}
.hat-card.white {{ border-color: #fff; }}
.hat-card.red {{ border-color: #ff4444; }}
.hat-card.black {{ border-color: #333; }}
.hat-card.yellow {{ border-color: #ffd700; }}
.hat-card.green {{ border-color: #00ff88; }}
.hat-card.blue {{ border-color: #0066ff; }}
.hat-icon {{ font-size: 2em; margin-bottom: 10px; }}
.hat-level {{ font-size: 1.5em; color: #00ff88; font-weight: bold; }}
.footer {{ text-align: center; padding: 30px; color: #555; border-top: 1px solid #333; margin-top: 30px; }}
@media (max-width: 600px) {{ .metrics {{ grid-template-columns: 1fr; }} .hats-grid {{ grid-template-columns: 1fr; }} }}
</style></head><body>
<div class="header">
<h1>🧠 Kimi-Code</h1>
<p>Adaptive Coding Mentor • Six Thinking Hats • Level {data['global_level']}</p>
</div>
<div class="metrics">
<div class="metric"><label>Level</label><span class="num">{data['global_level']}</span></div>
<div class="metric"><label>XP</label><span class="num">{data['global_xp']}</span></div>
<div class="metric"><label>🔥 Streak</label><span class="num">{data['streak']}</span></div>
<div class="metric"><label>Challenges</label><span class="num">{data['total_challenges']}</span></div>
</div>
<div class="section">
<h2>🎓 Skills</h2>
<div class="skill-grid">
{''.join([f'<div class="skill-item"><span class="skill-name">{k.replace("_", " ").title()}</span><div class="skill-bar"><div class="skill-fill" style="width:{v}%"></div></div><span class="skill-value">{v:.0f}</span></div>' for k, v in data['skill_tree'].items()])}
</div>
</div>
<div class="section">
<h2>🎩 Six Thinking Hats</h2>
<div class="hats-grid">
{''.join([f'<div class="hat-card {k}"><div class="hat-icon">{ {"white":"📊","red":"🔥","black":"⚠️","yellow":"✨","green":"🌱","blue":"🧠"}[k] }</div><div class="hat-level">L{ v["level"] }</div><div style="color:#888;font-size:0.8em;">{v["xp"]} XP • {v["challenges"]} challenges</div></div>' for k, v in data['hats_mastery'].items()])}
</div>
</div>
<div class="footer">
<p>Kimi-Code v1.0.0 • Training the next generation of developers</p>
<p>Synced with RootBase ecosystem</p>
</div>
</body></html>"""

        self._send_html(html)

    def _api_status(self, query):
        """API: System status."""
        self._send_json({
            "status": "running",
            "version": "1.0.0",
            "user_level": self.state.state["global_level"],
            "challenges_completed": self.state.state["total_challenges_completed"]
        })

    def _api_skills(self, query):
        """API: Skill data."""
        self._send_json(self.state.state["skill_tree"])

    def _api_hats(self, query):
        """API: Hat mastery data."""
        self._send_json(self.state.state["hats_mastery"])

    def _api_challenge(self, query):
        """API: Generate challenge."""
        lang = query.get('lang', ['python'])[0]
        diff = int(query.get('diff', ['5'])[0])

        from core.challenge_generator import ChallengeGenerator
        gen = ChallengeGenerator(self.state)
        challenge = gen.generate_challenge(lang, "basics", diff)

        self._send_json({
            "id": challenge.id,
            "title": challenge.title,
            "description": challenge.description,
            "difficulty": challenge.difficulty,
            "starter_code": challenge.starter_code,
            "time_limit": challenge.time_limit,
            "xp_reward": challenge.xp_reward
        })

    def _api_progress(self, query):
        """API: Full progress data."""
        self._send_json(self.state.get_dashboard_data())

    def _api_skill_tree(self, query):
        """API: Skill tree visualization data."""
        from core.skill_tree import SkillTree
        tree = SkillTree(self.state)
        self._send_json(tree.get_tree_visualization())

    def _serve_404(self, query):
        """404 handler."""
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error": "Not found"}).encode())

    def _send_html(self, html: str):
        """Send HTML response."""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode())

    def _send_json(self, data: dict):
        """Send JSON response."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

def start_dashboard(port: int, state_engine):
    """Start dashboard server."""
    def handler(*args, **kwargs):
        return DashboardHandler(state_engine, None, *args, **kwargs)

    server = HTTPServer(('', port), handler)
    print(f"Dashboard running at http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("
Shutting down...")
        server.shutdown()

def start_api_server(port: int, state_engine, api_bridge):
    """Start API server."""
    def handler(*args, **kwargs):
        return DashboardHandler(state_engine, api_bridge, *args, **kwargs)

    server = HTTPServer(('', port), handler)
    print(f"API server running at http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("
Shutting down...")
        server.shutdown()
