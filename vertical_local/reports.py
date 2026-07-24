from typing import Dict

HTML_TMPL = """<html><head><meta charset='utf-8'><title>Debate Report</title>
<style>body{font-family:Inter,Arial;background:#f6f8fb;color:#0f172a;padding:24px}h1{color:#0b1223}pre{white-space:pre-wrap;background:#fff;border-radius:8px;padding:12px;box-shadow:0 4px 14px rgba(12,20,40,.06)}</style>
</head><body>
<h1>Debate Report</h1>
<h2>Case</h2>
<pre>{case}</pre>
<h2>Scores</h2>
<ul>
{scores}
</ul>
<h2>Turns</h2>
{turns}
</body></html>"""


def render_report(report: Dict) -> str:
    scores_html = ''
    for pid, score in report.get('scores', {}).items():
        name = report.get('personas', {}).get(pid, {}).get('name', pid)
        scores_html += f"<li><strong>{name}</strong>: {score}</li>\n"

    turns_html = ''
    for t in report.get('turns', []):
        turns_html += f"<h3>Turn {t['turn']}</h3>\n"
        for e in t['entries']:
            turns_html += f"<div style='margin:6px 0;padding:8px;border-radius:6px;background:#fff'><strong>{e['name']}</strong><div style='font-size:13px'>{e['reply']}</div></div>\n"

    return HTML_TMPL.format(case=report.get('case',''), scores=scores_html, turns=turns_html)
