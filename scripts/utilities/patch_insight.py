
import pathlib

f = pathlib.Path.home() / "tools/codementor_cli/insight_v2.py"
src = f.read_text()

old1 = "    # [Implementation would call API based on CFG here]"
new1 = (
    '    req = urllib.request.Request(\n'
    '        f"https://generativelanguage.googleapis.com/v1beta/models/{CFG[\'model\']}:generateContent?key={CFG[\'api_key\']}",\n'
    '        data=json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode(),\n'
    '        headers={"Content-Type": "application/json"}\n'
    '    )\n'
    '    result = json.loads(urllib.request.urlopen(req).read())\n'
    '    explanation = result["candidates"][0]["content"]["parts"][0]["text"]'
)
src = src.replace(old1, new1) if old1 in src else src
print("P1:", "applied" if old1 in src or new1 in src else "not found")

old3 = '        # [Implementation would perform LLM query with context]\n        print("Insight: [LLM response]")'
new3 = (
    '        req = urllib.request.Request(\n'
    '            f"https://generativelanguage.googleapis.com/v1beta/models/{CFG[\'model\']}:generateContent?key={CFG[\'api_key\']}",\n'
    '            data=json.dumps({"contents": [{"parts": [{"text": f"File: {filepath}\\nContext:\\n{file_context}\\nQuestion: {query}"}]}]}).encode(),\n'
    '            headers={"Content-Type": "application/json"}\n'
    '        )\n'
    '        result = json.loads(urllib.request.urlopen(req).read())\n'
    '        print("Insight:", result["candidates"][0]["content"]["parts"][0]["text"])'
)
src = src.replace(old3, new3) if old3 in src else src
print("P3:", "applied" if old3 not in src else "not found")

old4 = '    return {"explanation": "...", "hotspots": ctx_parser.hotspots}'
new4 = '    return {"explanation": explanation, "hotspots": ctx_parser.hotspots}'
src = src.replace(old4, new4) if old4 in src else src
print("P4:", "applied" if old4 not in src else "not found")

old5 = "    # Initial analysis\n    analyze(filepath)"
new5 = "    file_context = pathlib.Path(filepath).read_text()\n    analyze(filepath)"
src = src.replace(old5, new5) if old5 in src else src
print("P5:", "applied" if old5 not in src else "not found")

f.write_text(src)
print("Done.")
