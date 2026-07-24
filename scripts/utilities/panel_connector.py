#!/usr/bin/env python3
"""
CodeMentor Panel Connector
The missing link between the Six Hats brain and the VS Code extension panel.

This is what was never built. The ChatGPT session described what the panel
should show. The Kimi engine generates that content. This file connects them.

The VS Code extension sends code to this module.
This module runs it through the Six Hats engine via the API bridge.
It returns structured HTML that the panel renders directly.

Usage from extension (via CallAIForExplanation.ts):
  POST /explain   { code, mode, language, tier }
  POST /compare   { code_a, code_b, language }     [PRO]
  POST /quiz      { code, language, difficulty }    [PRO]
  POST /hats      { code, sequence_mode }           [PRO]

Or run standalone for testing:
  python3 panel_connector.py --code "def hello(): print('hi')" --mode explain
"""

import sys
import json
import argparse
from typing import Optional, Dict, Any
from pathlib import Path

# Allow running from anywhere
sys.path.insert(0, str(Path(__file__).parent))

try:
    from core.six_hats import SixHatsEngine
    from core.state_engine import StateEngine
    from bridge.api_bridge import APIBridge, MentorResponse
except ImportError:
    # Fallback for standalone testing before extraction
    from six_hats import SixHatsEngine
    from state_engine import StateEngine
    from api_bridge import APIBridge, MentorResponse


class PanelConnector:
    """
    Translates VS Code extension requests into Six Hats analysis
    and returns panel-ready HTML.

    This is the handshake that was missing.
    """

    SYSTEM_PROMPT = """You are CodeMentor, an expert programming teacher embedded in a developer's IDE.
Your job is NOT to write code for them. Your job is to teach them to understand code deeply.

Rules:
- Be direct and specific. No filler phrases.
- Reference the actual code they gave you. Line numbers help.
- Always end with a concrete next step or challenge.
- Format in clean HTML with the structure provided.
- Match complexity to the developer's level.
- Never be condescending. Never be vague."""

    def __init__(self, data_dir: str = None):
        self.hats = SixHatsEngine()
        self.state = StateEngine(data_dir=data_dir or "/tmp/codementor_data")
        self.bridge = APIBridge()

    # ── TIER: FREE ────────────────────────────────────────────────────────────

    def explain(self, code: str, language: str = "python",
                level: str = "auto") -> Dict[str, Any]:
        """
        Free tier: Explain Mode.
        Overview + Step-by-step breakdown + Mentorship challenge.
        This is the core value prop — what makes CodeMentor different from Copilot.
        """
        if level == "auto":
            modifier = self.state.calculate_difficulty_modifier()
            level = "beginner" if modifier < 0.8 else "intermediate" if modifier < 1.4 else "advanced"

        prompt = f"""Analyze this {language} code for a {level} developer.

CODE:
```{language}
{code}
```

Return ONLY valid HTML with this exact structure — no markdown, no backticks:

<div class="cm-explain">
  <div class="cm-section cm-overview">
    <h3>📋 Overview</h3>
    <p>[2-3 sentences: what this code does and why it exists]</p>
  </div>

  <div class="cm-section cm-breakdown">
    <h3>🔍 Step-by-Step Breakdown</h3>
    <ol>
      [Each significant line or block. Be specific. Reference actual variable names and function calls.]
    </ol>
  </div>

  <div class="cm-section cm-bestpractice">
    <h3>⭐ Best Practice Note</h3>
    <p>[One specific improvement this code could make. Be direct.]</p>
  </div>

  <div class="cm-section cm-challenge">
    <h3>🎯 Mentorship Challenge</h3>
    <p>[One concrete task that would deepen their understanding. Specific, achievable.]</p>
  </div>
</div>"""

        result = self.bridge.generate(prompt, system=self.SYSTEM_PROMPT, max_tokens=1200)

        return self._build_response(
            mode="explain",
            content=result.content,
            success=result.success,
            backend=result.backend,
            error=result.error
        )

    # ── TIER: PRO ─────────────────────────────────────────────────────────────

    def compare(self, code_a: str, code_b: str,
                language: str = "python") -> Dict[str, Any]:
        """
        Pro tier: Compare Mode.
        Side-by-side analysis of two implementations.
        """
        prompt = f"""Compare these two {language} implementations for a developer learning best practices.

IMPLEMENTATION A:
```{language}
{code_a}
```

IMPLEMENTATION B:
```{language}
{code_b}
```

Return ONLY valid HTML:

<div class="cm-compare">
  <div class="cm-section cm-verdict">
    <h3>⚖️ Verdict</h3>
    <p>[Which is better overall and the single most important reason why]</p>
  </div>

  <div class="cm-section cm-differences">
    <h3>🔄 Key Differences</h3>
    <table class="cm-diff-table">
      <tr><th>Dimension</th><th>Implementation A</th><th>Implementation B</th></tr>
      [3-5 rows: readability, performance, error handling, maintainability, etc.]
    </table>
  </div>

  <div class="cm-section cm-tradeoffs">
    <h3>📊 Tradeoffs</h3>
    <p>[When would you choose A? When would you choose B?]</p>
  </div>

  <div class="cm-section cm-takeaway">
    <h3>🎯 What to Learn From This</h3>
    <p>[The one pattern or principle this comparison teaches]</p>
  </div>
</div>"""

        result = self.bridge.generate(prompt, system=self.SYSTEM_PROMPT, max_tokens=1400)

        return self._build_response(
            mode="compare",
            content=result.content,
            success=result.success,
            backend=result.backend,
            error=result.error
        )

    def quiz(self, code: str, language: str = "python",
             difficulty: int = 3) -> Dict[str, Any]:
        """
        Pro tier: Quiz Mode.
        Active learning questions based on the code.
        """
        prompt = f"""Generate a quiz for this {language} code at difficulty level {difficulty}/5.

CODE:
```{language}
{code}
```

Return ONLY valid HTML:

<div class="cm-quiz">
  <div class="cm-section cm-quiz-intro">
    <h3>🧠 Knowledge Check</h3>
    <p>[One sentence framing what this quiz tests]</p>
  </div>

  <div class="cm-section cm-questions">
    [3 questions, each in this format:]
    <div class="cm-question" data-question="1">
      <p class="cm-q-text"><strong>Q1:</strong> [Question text]</p>
      <div class="cm-options">
        <label><input type="radio" name="q1" value="a"> A) [Option]</label>
        <label><input type="radio" name="q1" value="b"> B) [Option]</label>
        <label><input type="radio" name="q1" value="c"> C) [Option]</label>
        <label><input type="radio" name="q1" value="d"> D) [Option]</label>
      </div>
      <div class="cm-answer" style="display:none">
        <p><strong>Answer:</strong> [Letter]) [Explanation of why]</p>
      </div>
    </div>
  </div>

  <button class="cm-reveal-btn" onclick="document.querySelectorAll('.cm-answer').forEach(a=>a.style.display='block')">
    Reveal Answers
  </button>
</div>"""

        result = self.bridge.generate(prompt, system=self.SYSTEM_PROMPT, max_tokens=1400)

        return self._build_response(
            mode="quiz",
            content=result.content,
            success=result.success,
            backend=result.backend,
            error=result.error
        )

    def six_hats_analysis(self, code: str, language: str = "python",
                          sequence_mode: str = "standard") -> Dict[str, Any]:
        """
        Pro tier: Full Six Hats analysis.
        The adversarial engine — looks at code from every angle.
        This is what destroys CodeRabbit.
        """
        sequence = self.hats.generate_sequence(sequence_mode)
        results = []

        for hat_name in sequence:
            hat_prompt = self.hats.generate_prompt_for_hat(hat_name, code)
            result = self.bridge.generate(
                hat_prompt,
                system=self.SYSTEM_PROMPT,
                max_tokens=600
            )
            if result.success:
                results.append({
                    "hat": hat_name,
                    "content": result.content
                })

        # Blue hat synthesis
        all_findings = "\n\n".join([
            f"=== {r['hat'].upper()} HAT ===\n{r['content'][:300]}"
            for r in results if r["hat"] != "blue"
        ])

        synthesis_prompt = f"""Given these Six Hats analyses of the code, write the Blue Hat synthesis.

{all_findings}

Return ONLY a Blue Hat HTML section:
<div class="cm-hat cm-blue-hat">
  <h3>🧠 Blue Hat: Action Plan</h3>
  <div class="cm-priorities">
    <h4>Priority Actions</h4>
    <ol>[3-5 specific, ordered action items based on all hat findings]</ol>
  </div>
  <div class="cm-verdict">
    <h4>Overall Assessment</h4>
    <p>[2-3 sentences synthesizing everything]</p>
  </div>
</div>"""

        synthesis = self.bridge.generate(synthesis_prompt, system=self.SYSTEM_PROMPT, max_tokens=500)
        if synthesis.success:
            results.append({"hat": "blue_synthesis", "content": synthesis.content})

        # Combine all hat HTML into one panel response
        combined_html = self._build_hats_html(results)

        return self._build_response(
            mode="six_hats",
            content=combined_html,
            success=True,
            backend=self.bridge.active_backend,
            metadata={"sequence": sequence, "hats_completed": len(results)}
        )

    # ── HELPERS ───────────────────────────────────────────────────────────────

    def _build_hats_html(self, results: list) -> str:
        hat_colors = {
            "white": "#f5f5f5",
            "red": "#ff4444",
            "black": "#333333",
            "yellow": "#ffd700",
            "green": "#00cc66",
            "blue": "#0066ff",
            "blue_synthesis": "#0066ff"
        }

        sections = []
        for r in results:
            color = hat_colors.get(r["hat"], "#888")
            sections.append(
                f'<div class="cm-hat" style="border-left: 4px solid {color}; padding: 12px; margin: 8px 0;">'
                f'{r["content"]}'
                f'</div>'
            )

        return (
            '<div class="cm-six-hats">'
            '<h2>Six Thinking Hats Analysis</h2>'
            + "".join(sections) +
            '</div>'
        )

    def _build_response(self, mode: str, content: str, success: bool,
                        backend: str = "", error: str = None,
                        metadata: Dict = None) -> Dict[str, Any]:
        """Standard response envelope for VS Code extension consumption."""
        return {
            "success": success,
            "mode": mode,
            "html": content if success else self._error_html(error or "Analysis failed"),
            "backend": backend,
            "error": error,
            "metadata": metadata or {}
        }

    def _error_html(self, message: str) -> str:
        return f"""<div class="cm-error">
  <h3>⚠️ CodeMentor Error</h3>
  <p>{message}</p>
  <p>Check that Ollama is running: <code>ollama serve</code></p>
  <p>Or set ANTHROPIC_API_KEY for Claude backend.</p>
</div>"""


# ── CLI for testing ───────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="CodeMentor Panel Connector")
    parser.add_argument("--code", type=str, help="Code to analyze")
    parser.add_argument("--file", type=str, help="File to analyze")
    parser.add_argument("--mode", choices=["explain", "compare", "quiz", "hats"],
                        default="explain")
    parser.add_argument("--language", default="python")
    parser.add_argument("--sequence", default="standard",
                        choices=["standard", "quick", "deep", "random"])
    args = parser.parse_args()

    code = ""
    if args.file:
        code = Path(args.file).read_text()
    elif args.code:
        code = args.code
    else:
        # Default test code
        code = '''def get_user(username):
    query = f"SELECT * FROM users WHERE username=\'{username}\'"
    return db.execute(query)'''

    connector = PanelConnector()

    print(f"CodeMentor Panel Connector")
    print(f"Mode: {args.mode} | Backend: {connector.bridge.active_backend}")
    print("=" * 50)

    if args.mode == "explain":
        result = connector.explain(code, args.language)
    elif args.mode == "compare":
        # For CLI testing, compare code with itself (demo)
        result = connector.compare(code, code + "\n# Alternative", args.language)
    elif args.mode == "quiz":
        result = connector.quiz(code, args.language)
    elif args.mode == "hats":
        result = connector.six_hats_analysis(code, args.language, args.sequence)

    if result["success"]:
        print(result["html"])
    else:
        print(f"ERROR: {result['error']}")

    print()
    print(f"Backend used: {result['backend']}")


if __name__ == "__main__":
    main()
