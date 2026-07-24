#!/usr/bin/env python3
"""
CodeMentor AI Engine + Analytics Toolkit
Free/open-source integrations: matplotlib, pandas, numpy, ast, radon, bandit
"""
import sys, os, json, urllib.request, pathlib, hashlib, re, ast, textwrap
from datetime import datetime

# --- CONFIG ---
BASE_DIR = "/storage/emulated/0/RootBase/CodeMentor-MVP"
CONFIG_PATH = f"{BASE_DIR}/config/api.json"
CACHE_DIR = f"{BASE_DIR}/cache"
ANALYTICS_DIR = f"{BASE_DIR}/analytics"
pathlib.Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)
pathlib.Path(ANALYTICS_DIR).mkdir(parents=True, exist_ok=True)

# --- CACHE SYSTEM ---
def get_cache_key(code, mode="explain"):
    return f"{mode}_{hashlib.sha256(code.encode()).hexdigest()[:16]}"

def check_cache(key):
    p = pathlib.Path(CACHE_DIR) / f"{key}.json"
    if p.exists():
        return json.loads(p.read_text())
    return None

def save_cache(key, data):
    (pathlib.Path(CACHE_DIR) / f"{key}.json").write_text(json.dumps(data))

# --- ANALYTICS ENGINE ---
def analyze_code(code, filepath="unknown"):
    """Static analysis + metrics generation (no external deps required)"""
    lines = code.split('\n')
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "filepath": filepath,
        "total_lines": len(lines),
        "code_lines": len([l for l in lines if l.strip() and not l.strip().startswith('#')]),
        "comment_lines": len([l for l in lines if l.strip().startswith('#')]),
        "blank_lines": len([l for l in lines if not l.strip()]),
        "functions": [],
        "classes": [],
        "imports": [],
        "complexity_estimate": 0,
        "security_flags": []
    }
    
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                metrics["functions"].append({
                    "name": node.name,
                    "args": len(node.args.args),
                    "line": node.lineno,
                    "complexity": len(list(ast.walk(node)))
                })
                metrics["complexity_estimate"] += len(list(ast.walk(node)))
            elif isinstance(node, ast.ClassDef):
                metrics["classes"].append({
                    "name": node.name,
                    "methods": len([n for n in ast.walk(node) if isinstance(n, ast.FunctionDef)]),
                    "line": node.lineno
                })
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    metrics["imports"].append(alias.name)
    except SyntaxError:
        metrics["parse_error"] = True
    
    # Security heuristics
    risky = ['eval(', 'exec(', 'subprocess.call', 'os.system(', '__import__', 'input(', 'pickle.loads']
    for risk in risky:
        if risk in code:
            metrics["security_flags"].append(f"Potential risk: {risk}")
    
    return metrics

def generate_analytics_html(metrics):
    """Generate HTML dashboard from metrics"""
    func_rows = "".join([
        f'<tr><td>{f["name"]}</td><td>{f["args"]}</td><td>{f["line"]}</td><td>{f["complexity"]}</td></tr>' 
        for f in metrics["functions"]
    ]) or '<tr><td colspan="4">No functions found</td></tr>'
    
    class_rows = "".join([
        f'<tr><td>{c["name"]}</td><td>{c["methods"]}</td><td>{c["line"]}</td></tr>'
        for c in metrics["classes"]
    ]) or '<tr><td colspan="3">No classes found</td></tr>'
    
    sec_flags = "".join([f'<li class="warning">{f}</li>' for f in metrics["security_flags"]]) or '<li>No security flags</li>'
    
    return f'''
    <div class="analytics-dashboard">
        <h3>📊 Code Analytics Dashboard</h3>
        <div class="metrics-grid">
            <div class="metric"><span class="num">{metrics["total_lines"]}</span><label>Total Lines</label></div>
            <div class="metric"><span class="num">{metrics["code_lines"]}</span><label>Code Lines</label></div>
            <div class="metric"><span class="num">{metrics["comment_lines"]}</span><label>Comments</label></div>
            <div class="metric"><span class="num">{len(metrics["functions"])}</span><label>Functions</label></div>
            <div class="metric"><span class="num">{len(metrics["classes"])}</span><label>Classes</label></div>
            <div class="metric"><span class="num">{metrics["complexity_estimate"]}</span><label>Complexity Score</label></div>
        </div>
        <h4>Functions</h4>
        <table><thead><tr><th>Name</th><th>Args</th><th>Line</th><th>Complexity</th></tr></thead><tbody>{func_rows}</tbody></table>
        <h4>Classes</h4>
        <table><thead><tr><th>Name</th><th>Methods</th><th>Line</th></tr></thead><tbody>{class_rows}</tbody></table>
        <h4>🔒 Security Audit</h4>
        <ul>{sec_flags}</ul>
        <h4>Imports</h4>
        <code>{', '.join(metrics["imports"]) or 'None detected'}</code>
    </div>
    <style>
        .analytics-dashboard {{ background:#1a1a2e; color:#eee; padding:20px; border-radius:8px; font-family:monospace; }}
        .metrics-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:15px; margin-bottom:20px; }}
        .metric {{ text-align:center; background:#16213e; padding:15px; border-radius:6px; }}
        .num {{ font-size:2em; color:#00ff88; display:block; }}
        label {{ font-size:0.8em; color:#888; }}
        table {{ width:100%; border-collapse:collapse; margin:10px 0; }}
        th, td {{ padding:8px; text-align:left; border-bottom:1px solid #333; }}
        th {{ color:#00ff88; }}
        .warning {{ color:#ff4444; }}
        h4 {{ color:#00ccff; margin-top:20px; }}
    </style>
    '''

# --- AI EXPLANATION ENGINE ---
def load_config():
    if not os.path.exists(CONFIG_PATH):
        return None
    with open(CONFIG_PATH) as f:
        return json.load(f)

def call_gemini(code, api_key, model="gemini-2.0-flash"):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    prompt = f"""You are an expert Code Tutor and Security Analyst. Explain this code using ONLY HTML tags.
Structure:
<h3>Overview and Purpose</h3>
<h3>Step-by-Step Breakdown</h3>  
<h3>Security & Best Practices</h3>
<h3>Mentorship Challenge</h3>
Code: ```{code}```"""
    body = json.dumps({"contents":[{"parts":[{"text":prompt}]}]}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            resp = json.loads(r.read())
            return resp["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"<h3>Error</h3><p>API Error: {e}</p><p>Check your API key or network.</p>"

def call_openrouter(code, api_key, model="anthropic/claude-3.5-sonnet"):
    """Fallback to OpenRouter (pay-as-you-go, no Google account needed)"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://codementor.local",
        "X-Title": "CodeMentor MVP"
    }
    body = json.dumps({
        "model": model,
        "messages": [{"role":"user","content":f"Explain this code in HTML format with h3 headings: Overview, Breakdown, Security, Challenge. Code: ```{code}```"}]
    }).encode()
    req = urllib.request.Request(url, data=body, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            resp = json.loads(r.read())
            return resp["choices"][0]["message"]["content"]
    except Exception as e:
        return f"<h3>Error</h3><p>OpenRouter Error: {e}</p>"

# --- CHART GENERATION (matplotlib if available, else SVG fallback) ---
def generate_complexity_chart(metrics, output_path):
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        
        fig, axes = plt.subplots(2, 2, figsize=(10, 8))
        fig.patch.set_facecolor('#1a1a2e')
        
        # Lines breakdown pie
        ax1 = axes[0,0]
        sizes = [metrics["code_lines"], metrics["comment_lines"], metrics["blank_lines"]]
        labels = ['Code', 'Comments', 'Blank']
        colors = ['#00ff88', '#00ccff', '#333']
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', textprops={'color':'white'})
        ax1.set_title('Line Composition', color='white')
        
        # Function complexity bar
        ax2 = axes[0,1]
        if metrics["functions"]:
            names = [f["name"][:15] for f in metrics["functions"]]
            compl = [f["complexity"] for f in metrics["functions"]]
            ax2.barh(names, compl, color='#ff6b6b')
            ax2.set_title('Function Complexity', color='white')
            ax2.tick_params(colors='white')
        
        # Complexity trend (mock historical)
        ax3 = axes[1,0]
        x = np.arange(1, 6)
        y = [metrics["complexity_estimate"] * (0.8 + i*0.1) for i in range(5)]
        ax3.plot(x, y, 'o-', color='#ffd93d', linewidth=2)
        ax3.set_title('Complexity Trend (Mock)', color='white')
        ax3.set_facecolor('#16213e')
        ax3.tick_params(colors='white')
        
        # Security score gauge
        ax4 = axes[1,1]
        score = max(0, 100 - len(metrics["security_flags"]) * 25)
        ax4.bar(['Security Score'], [score], color='#00ff88' if score > 70 else '#ff4444')
        ax4.set_ylim(0, 100)
        ax4.set_title(f'Security: {score}/100', color='white')
        ax4.tick_params(colors='white')
        
        plt.tight_layout()
        plt.savefig(output_path, facecolor='#1a1a2e', dpi=150)
        plt.close()
        return f'<img src="file://{output_path}" style="max-width:100%;border-radius:8px;" />'
    except ImportError:
        # SVG fallback — no deps needed
        max_c = max([f["complexity"] for f in metrics["functions"]] or [1])
        bars = "".join([
            f'<rect x="{i*60+10}" y="{200-f["complexity"]*2}" width="50" height="{f["complexity"]*2}" fill="#00ff88" opacity="0.8"/>'
            f'<text x="{i*60+35}" y="220" fill="#fff" font-size="10" text-anchor="middle">{f["name"][:8]}</text>'
            for i, f in enumerate(metrics["functions"])
        ]) if metrics["functions"] else '<text x="150" y="100" fill="#888">No functions to chart</text>'
        
        svg = f'''<svg width="400" height="250" style="background:#1a1a2e;border-radius:8px;">
            <text x="200" y="30" fill="#00ff88" text-anchor="middle" font-size="16">Function Complexity</text>
            {bars}
        </svg>'''
        svg_path = output_path.replace('.png', '.svg')
        pathlib.Path(svg_path).write_text(svg)
        return svg

# --- MAIN ENTRY ---
def main():
    if len(sys.argv) < 2:
        print("Usage: ai_explain.py <file> [line_start] [line_end] [--analytics-only|--chart]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    mode = "explain"
    start = end = None
    
    for arg in sys.argv[2:]:
        if arg == "--analytics-only": mode = "analytics"
        elif arg == "--chart": mode = "chart"
        elif arg.startswith("--"): pass
        elif start is None: start = int(arg)
        else: end = int(arg)
    
    with open(filepath) as f:
        lines = f.readlines()
    
    if start and end:
        code = "".join(lines[start-1:end])
    else:
        code = "".join(lines)
    
    # Always run analytics
    metrics = analyze_code(code, filepath)
    metrics_file = f"{ANALYTICS_DIR}/{pathlib.Path(filepath).stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    pathlib.Path(metrics_file).write_text(json.dumps(metrics, indent=2))
    
    if mode == "analytics":
        print(generate_analytics_html(metrics))
        return
    
    if mode == "chart":
        chart_path = f"{ANALYTICS_DIR}/{pathlib.Path(filepath).stem}_chart.png"
        chart = generate_complexity_chart(metrics, chart_path)
        print(f"<h3>📈 Complexity Chart</h3>{chart}")
        return
    
    # Full mode: AI + Analytics
    cache_key = get_cache_key(code, "full")
    cached = check_cache(cache_key)
    
    if cached:
        explanation = cached["explanation"]
        print("<!-- CACHED -->")
    else:
        cfg = load_config()
        if not cfg:
            print("<h3>Error</h3><p>No API config. Run: mentor --setup</p>")
            sys.exit(1)
        
        if cfg.get("provider") == "openrouter":
            explanation = call_openrouter(code, cfg["api_key"], cfg.get("model", "anthropic/claude-3.5-sonnet"))
        else:
            explanation = call_gemini(code, cfg["api_key"], cfg.get("model", "gemini-2.0-flash"))
        
        save_cache(cache_key, {"explanation": explanation, "metrics": metrics, "timestamp": datetime.now().isoformat()})
    
    # Combine everything
    analytics_html = generate_analytics_html(metrics)
    chart_path = f"{ANALYTICS_DIR}/{pathlib.Path(filepath).stem}_chart.png"
    chart_html = generate_complexity_chart(metrics, chart_path)
    
    full_output = f'''
    <div class="codementor-report">
        {analytics_html}
        <hr style="border-color:#333;margin:30px 0;">
        {chart_html}
        <hr style="border-color:#333;margin:30px 0;">
        {explanation}
    </div>
    <style>
        .codementor-report {{ background:#0f0f1e; color:#e0e0e0; padding:30px; font-family:'Segoe UI',monospace; line-height:1.6; }}
        h3 {{ color:#00ff88; border-bottom:2px solid #00ff88; padding-bottom:8px; }}
        code {{ background:#1a1a2e; padding:2px 6px; border-radius:4px; color:#ffd93d; }}
        pre {{ background:#1a1a2e; padding:15px; border-radius:8px; overflow-x:auto; border:1px solid #333; }}
    </style>
    '''
    print(full_output)

if __name__ == "__main__":
    main()
