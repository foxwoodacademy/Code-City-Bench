#!/usr/bin/env python3
"""Scheduled scanner wrapper: runs bardildo summary and writes JSON to $TMPDIR
"""
import os
import subprocess
import json
from datetime import datetime
from pathlib import Path

ROOT = os.environ.get('BARD_ROOT', '/storage/emulated/0/RootBase')
TMP = os.environ.get('TMPDIR') or '/data/data/com.termux/files/usr/tmp'
OUT_DIR = Path(os.environ.get('BARD_OUTDIR') or TMP)
OUT_DIR.mkdir(parents=True, exist_ok=True)

SCRIPT = str(Path(__file__).parent / 'bardildo.py')

def run_summary():
    # run bardildo in non-write mode to get summary JSON from stdout
    cmd = ["python3", SCRIPT, "--root", ROOT]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        print('Error running bardildo:', proc.stderr)
        return None
    # bardildo prints a final JSON summary; try to parse last JSON block
    out = proc.stdout
    # heuristic: find first '{' of JSON
    idx = out.find('{')
    if idx == -1:
        print('No JSON summary found')
        return None
    try:
        j = json.loads(out[idx:])
    except Exception as e:
        print('JSON parse error:', e)
        return None
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    outfile = OUT_DIR / f'bardildo_summary_{ts}.json'
    outfile.write_text(json.dumps(j, indent=2), encoding='utf-8')
    print('Wrote summary to', outfile)
    return outfile

if __name__ == '__main__':
    run_summary()
