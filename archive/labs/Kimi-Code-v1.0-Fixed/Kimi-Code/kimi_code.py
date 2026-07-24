#!/usr/bin/env python3
"""
Kimi-Code: Adaptive Coding Mentor CLI
Six Thinking Hats • Progressive Difficulty • Multi-Language • Persistent State
"""
import sys
import os
import json
import argparse
from pathlib import Path

# Add core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from state_engine import StateEngine
from progression_engine import ProgressionEngine
from challenge_generator import ChallengeGenerator
from six_hats import SixHatsEngine
from api_bridge import APIBridge
from skill_tree import SkillTree

class KimiCode:
    """Main Kimi-Code application."""

    VERSION = "1.0.0"
    BANNER = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║   🧠 Kimi-Code v{version}                                    ║
    ║   Adaptive Coding Mentor • Six Thinking Hats                 ║
    ║                                                              ║
    ║   "Training the next generation of developers"               ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """

    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)

        self.state = StateEngine(self.data_dir)
        self.progression = ProgressionEngine(self.state)
        self.challenges = ChallengeGenerator(self.state)
        self.hats = SixHatsEngine(self.state)
        self.api = APIBridge()
        self.skill_tree = SkillTree(self.state)

    def run(self):
        """Main entry point."""
        parser = argparse.ArgumentParser(
            description='Kimi-Code: Adaptive Coding Mentor',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  kimi-code --setup                    Configure API keys
  kimi-code --status                   Show current progress
  kimi-code --challenge python         Start Python challenge
  kimi-code --hats-mode python         Six Hats analysis mode
  kimi-code --explain file.py          Explain code with AI
  kimi-code --skill-tree               View skill progression
  kimi-code --dashboard                Start web dashboard
  kimi-code --serve                    Start API server
            """
        )

        parser.add_argument('--setup', action='store_true', help='Configure API providers')
        parser.add_argument('--status', action='store_true', help='Show user status')
        parser.add_argument('--challenge', metavar='LANG', help='Start challenge in language')
        parser.add_argument('--track', default='basics', help='Challenge track (default: basics)')
        parser.add_argument('--difficulty', type=int, help='Force difficulty level')
        parser.add_argument('--hats-mode', metavar='LANG', help='Six Hats challenge mode')
        parser.add_argument('--hat', choices=['white','red','black','yellow','green','blue'], 
                          help='Focus on specific hat')
        parser.add_argument('--explain', metavar='FILE', help='Explain a code file')
        parser.add_argument('--mode', default='standard', 
                          choices=['standard','detailed','beginner','expert','security','performance','review'],
                          help='Explanation mode')
        parser.add_argument('--skill-tree', action='store_true', help='View skill tree')
        parser.add_argument('--unlock', metavar='NODE', help='Unlock skill node')
        parser.add_argument('--level-up', metavar='NODE', help='Level up skill node')
        parser.add_argument('--dashboard', action='store_true', help='Start web dashboard')
        parser.add_argument('--serve', action='store_true', help='Start API server')
        parser.add_argument('--port', type=int, default=8767, help='Server port')
        parser.add_argument('--report', action='store_true', help='Generate progress report')
        parser.add_argument('--sync', action='store_true', help='Sync with RootBase/CodeMentor')
        parser.add_argument('--version', action='store_true', help='Show version')

        args = parser.parse_args()

        if args.version:
            print(self.BANNER.format(version=self.VERSION))
            return

        if args.setup:
            self._setup()
        elif args.status:
            self._show_status()
        elif args.challenge:
            self._start_challenge(args.challenge, args.track, args.difficulty, hat_focus=args.hat)
        elif args.hats_mode:
            self._start_hats_mode(args.hats_mode, args.track, args.difficulty)
        elif args.explain:
            self._explain_file(args.explain, args.mode)
        elif args.skill_tree:
            self._show_skill_tree()
        elif args.unlock:
            self._unlock_node(args.unlock)
        elif args.level_up:
            self._level_up_node(args.level_up)
        elif args.dashboard:
            self._start_dashboard(args.port)
        elif args.serve:
            self._start_server(args.port)
        elif args.report:
            self._generate_report()
        elif args.sync:
            self._sync_rootbase()
        else:
            print(self.BANNER.format(version=self.VERSION))
            parser.print_help()

    def _setup(self):
        """Interactive setup."""
        print("🧠 Kimi-Code Setup")
        print("=" * 50)

        print("
1. Kimi API (Primary - Recommended)")
        kimi_key = input("   Kimi API Key (or press Enter to skip): ").strip()
        if kimi_key:
            self.api.set_provider_key("kimi", kimi_key)
            print("   ✓ Kimi configured")

        print("
2. Gemini (Fallback)")
        gemini_key = input("   Gemini API Key (or press Enter to skip): ").strip()
        if gemini_key:
            self.api.set_provider_key("gemini", gemini_key)
            print("   ✓ Gemini configured")

        print("
3. OpenRouter (Alternative)")
        or_key = input("   OpenRouter Key (or press Enter to skip): ").strip()
        if or_key:
            self.api.set_provider_key("openrouter", or_key)
            print("   ✓ OpenRouter configured")

        print("
4. Preferences")
        lang = input("   Primary language [python]: ").strip() or "python"
        self.state.state["preferences"]["primary_language"] = lang

        curve = input("   Difficulty curve [adaptive/linear/aggressive]: ").strip() or "adaptive"
        self.state.state["preferences"]["difficulty_curve"] = curve

        self.state.save()
        print("
✅ Setup complete! Run `kimi-code --status` to verify.")

    def _show_status(self):
        """Display user status dashboard."""
        data = self.state.get_dashboard_data()

        print(f"""
    ┌─────────────────────────────────────────┐
    │  🧠 Kimi-Code Status                    │
    ├─────────────────────────────────────────┤
    │  Level: {data['global_level']:<3}    XP: {data['global_xp']:<8}    │
    │  🔥 Streak: {data['streak']:<3} days                  │
    │  📊 Challenges: {data['total_challenges']:<4}              │
    │  ⚡ Difficulty Modifier: {data['difficulty_modifier']:.2f}       │
    └─────────────────────────────────────────┘
        """)

        print("
🎓 Skill Tree:")
        for skill, level in data['skill_tree'].items():
            bar = "█" * int(level / 5) + "░" * (20 - int(level / 5))
            print(f"   {skill:<25} [{bar}] {level:.1f}")

        print("
🎩 Hat Mastery:")
        for hat, stats in data['hats'].items():
            bar = "█" * stats['level'] + "░" * (10 - stats['level'])
            print(f"   {hat.capitalize():<10} [{bar}] L{stats['level']} XP:{stats['xp']}")

        print("
💻 Languages:")
        for lang, info in data['languages'].items():
            print(f"   {lang.capitalize():<12} Level {info['level']} | Mastery {info['mastery']:.0%}")

        if data['achievements']:
            print("
🏆 Achievements:")
            for ach in data['achievements'][-5:]:
                print(f"   ✓ {ach}")

    def _start_challenge(self, language: str, track: str, difficulty: int = None, 
                        hat_focus: str = None):
        """Start a coding challenge."""
        if not difficulty:
            _, difficulty = self.progression.get_recommended_difficulty(language)

        print(f"
🎯 Generating {language} challenge (difficulty: {difficulty}/15)...")

        challenge = self.challenges.generate_challenge(
            language, track, difficulty, hat_focus
        )

        print(f"""
    ┌─────────────────────────────────────────┐
    │  Challenge: {challenge.title:<29}│
    │  Type: {challenge.challenge_type:<34}│
    │  Difficulty: {'★' * challenge.difficulty:<25}│
    │  XP Reward: {challenge.xp_reward:<28}│
    │  Time Limit: {challenge.time_limit // 60}m {challenge.time_limit % 60}s{'':18}│
    └─────────────────────────────────────────┘
        """)

        if challenge.hat_focus:
            hat = self.hats.get_hat(challenge.hat_focus)
            print(f"
🎩 {hat.emoji} {hat.role} Mode")
            print(f"   Focus: {hat.focus}")

        print(f"
📋 Description:
{challenge.description}
")
        print("📝 Starter Code:")
        print("-" * 50)
        print(challenge.starter_code)
        print("-" * 50)

        # Interactive challenge loop would go here
        print("
💡 Type your solution and press Ctrl+D when done (or save to /tmp/solution.py)")
        print("   (Interactive mode - implement full challenge loop in production)")

    def _start_hats_mode(self, language: str, track: str, difficulty: int = None):
        """Start Six Thinking Hats challenge sequence."""
        print("
🎩 Six Thinking Hats Mode")
        print("=" * 50)

        sequence = self.hats.generate_sequence("standard")
        print(f"Sequence: {' → '.join([h.title() for h in sequence])}
")

        for i, hat_name in enumerate(sequence):
            hat = self.hats.get_hat(hat_name)
            print(f"
{'='*50}")
            print(f"Hat {i+1}/{len(sequence)}: {hat.emoji} {hat.hat.title()} Hat")
            print(f"Role: {hat.role}")
            print(f"Focus: {hat.focus}")
            print(f"{'='*50}
")

            # Generate challenge for this hat
            if not difficulty:
                _, difficulty = self.progression.get_recommended_difficulty(language)

            challenge = self.challenges.generate_challenge(
                language, track, difficulty, hat_name
            )

            print(f"Challenge: {challenge.title}")
            print(f"{challenge.description}
")

            # In full implementation, this would wait for user input
            print("   [Press Enter to continue to next hat...]")
            input()

        print("
✅ Sequence complete! Blue Hat synthesis saved.")

    def _explain_file(self, filepath: str, mode: str):
        """Explain a code file using AI."""
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            return

        with open(filepath, 'r') as f:
            code = f.read()

        language = Path(filepath).suffix.lstrip('.')

        print(f"🧠 Analyzing {filepath}...")

        # Get user context for enhanced prompting
        context = {
            "user_level": self.state.state["global_level"],
            "weak_skills": [
                k for k, v in self.state.state["skill_tree"].items() 
                if v < 50
            ],
            "strong_skills": [
                k for k, v in self.state.state["skill_tree"].items() 
                if v > 75
            ]
        }

        result = self.api.explain_code(code, language, mode, 
                                      hats_mode=self.state.state["preferences"].get("six_hats_mode", False),
                                      context=context)

        print("
" + "=" * 60)
        print(result["explanation"])
        print("=" * 60)

        # Save to analytics
        self.state.log_challenge({
            "type": "explanation",
            "language": language,
            "mode": mode,
            "file": filepath,
            "provider": result["provider_used"],
            "success": True,
            "time_taken": 0,
            "complexity": 5
        })

    def _show_skill_tree(self):
        """Display skill tree visualization."""
        viz = self.skill_tree.get_tree_visualization()

        print("
🌳 Skill Tree")
        print("=" * 60)

        categories = {}
        for node in viz["nodes"]:
            cat = node["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(node)

        for cat, nodes in categories.items():
            print(f"
📁 {cat.upper()}")
            for node in nodes:
                status = "🔓" if node["completed"] else ("✅" if node["unlocked"] else "🔒")
                level = f"L{node['level']}/{node['max_level']}" if node["unlocked"] else "Locked"
                print(f"   {status} {node['icon']} {node['name']:<25} {level}")

        # Show available unlocks
        available = self.skill_tree.get_available_nodes()
        if available:
            print("
🔓 Available to Unlock:")
            for node in available:
                print(f"   {node['icon']} {node['name']} (Cost: {node['xp_cost']} XP)")

    def _unlock_node(self, node_id: str):
        """Unlock a skill node."""
        if self.skill_tree.unlock_node(node_id):
            print(f"✅ Unlocked: {node_id}")
        else:
            print(f"❌ Cannot unlock {node_id}. Check prerequisites and XP.")

    def _level_up_node(self, node_id: str):
        """Level up a skill node."""
        if self.skill_tree.level_up_node(node_id):
            print(f"✅ Leveled up: {node_id}")
        else:
            print(f"❌ Cannot level up {node_id}. Check unlock status and XP.")

    def _start_dashboard(self, port: int):
        """Start web dashboard."""
        print(f"🌐 Starting dashboard on http://localhost:{port}")

        # Import and start dashboard server
        try:
            from bridges.api_server import start_dashboard
            start_dashboard(port, self.state)
        except ImportError:
            print("Dashboard module not available. Run: pip install -r requirements.txt")

    def _start_server(self, port: int):
        """Start API server."""
        print(f"🚀 Starting API server on http://localhost:{port}")

        try:
            from bridges.api_server import start_api_server
            start_api_server(port, self.state, self.api)
        except ImportError:
            print("API server module not available.")

    def _generate_report(self):
        """Generate comprehensive progress report."""
        report = self.progression.get_progress_summary()

        report_file = os.path.join(self.data_dir, 
                                  f"report_{self.state.state['user_id'][:8]}.html")

        # Generate HTML report
        html = self._build_report_html(report)

        with open(report_file, 'w') as f:
            f.write(html)

        print(f"📊 Report saved: {report_file}")

    def _build_report_html(self, report: dict) -> str:
        """Build HTML progress report."""
        return f"""<!DOCTYPE html>
<html><head><title>Kimi-Code Progress Report</title>
<style>
body {{ font-family: 'Segoe UI', sans-serif; background: #0f0f1e; color: #e0e0e0; padding: 40px; }}
h1 {{ color: #00ff88; }} h2 {{ color: #60a5fa; }}
.metric {{ display: inline-block; background: #1a1a2e; padding: 20px; margin: 10px; border-radius: 10px; }}
.metric .num {{ font-size: 2.5em; color: #00ff88; }}
.skill-bar {{ background: #333; height: 20px; border-radius: 10px; margin: 5px 0; }}
.skill-fill {{ background: linear-gradient(90deg, #00ff88, #60a5fa); height: 100%; border-radius: 10px; }}
table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #333; }}
th {{ color: #00ff88; background: #1a1a2e; }}
</style></head><body>
<h1>🧠 Kimi-Code Progress Report</h1>
<div class="metric"><span class="num">{report['global']['level']}</span><div>Level</div></div>
<div class="metric"><span class="num">{report['global']['xp']}</span><div>Total XP</div></div>
<div class="metric"><span class="num">{report['global']['streak']}</span><div>Day Streak</div></div>
<h2>Skills</h2>
{''.join([f'<div>{k}: <div class="skill-bar"><div class="skill-fill" style="width:{v}%"></div></div></div>' for k, v in report['skills'].items()])}
<h2>Hat Mastery</h2>
<table><tr><th>Hat</th><th>Level</th><th>XP</th><th>Challenges</th></tr>
{''.join([f'<tr><td>{k.capitalize()}</td><td>{v["level"]}</td><td>{v["xp"]}</td><td>{v["challenges"]}</td></tr>' for k, v in report['hats'].items()])}
</table>
<p style="margin-top:40px;color:#888;">Generated: {self.state.state['last_session']}</p>
</body></html>"""

    def _sync_rootbase(self):
        """Sync with RootBase/CodeMentor ecosystem."""
        print("🔄 Syncing with RootBase...")

        try:
            from bridges.rootbase_sync import RootBaseSync
            sync = RootBaseSync(self.state)
            sync.sync_all()
            print("✅ Sync complete")
        except ImportError:
            print("⚠️ RootBase sync module not available")
            print("   Manual sync: Copy data/ directory to /storage/emulated/0/RootBase/Kimi-Code/")

if __name__ == "__main__":
    app = KimiCode()
    app.run()
