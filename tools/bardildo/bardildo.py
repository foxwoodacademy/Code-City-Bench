#!/usr/bin/env python3
"""Bardildo: scans a repo and writes per-folder manifest.json and runbook.txt

Usage: python3 bardildo.py --root /path/to/workspace --write
"""
import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

VOICE = {
    'name': 'Bardildo',
    'tone': 'rude',
}

SKIP_DIRS = {'.git', 'node_modules', '__pycache__', 'tools', 'archive'}

EXT_LANG = {
    '.py': 'python', '.js': 'javascript', '.ts': 'typescript', '.jsx': 'javascript', '.tsx': 'typescript',
    '.go': 'go', '.rs': 'rust', '.java': 'java', '.html': 'html', '.css': 'css'
}

COMMON_ENTRYPOINTS = [
    'main.py', 'app.py', 'server.py', 'index.py', 'run.sh', 'start.sh', 'package.json', 'vite.config.js'
]


def detect_languages(path: Path):
    counts = {}
    for root, dirs, files in os.walk(path):
        for f in files:
            ext = Path(f).suffix.lower()
            lang = EXT_LANG.get(ext)
            if lang:
                counts[lang] = counts.get(lang, 0) + 1
    return counts


def read_first_readme(path: Path):
    candidates = ['README.md', 'README', 'README.txt']
    for c in candidates:
        p = path / c
        if p.exists():
            try:
                with p.open('r', encoding='utf-8') as fh:
                    text = fh.read(2000)
                    return text.strip().split('\n')[0:5]
            except Exception:
                return None
    return None


def find_entrypoints(path: Path):
    found = []
    for name in COMMON_ENTRYPOINTS:
        if (path / name).exists():
            found.append(name)
    # fallback: any .py as entry
    for f in path.iterdir():
        if f.is_file() and f.suffix == '.py' and f.name not in ('setup.py',):
            found.append(f.name)
            break
    return found


def read_package_json(path: Path):
    p = path / 'package.json'
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding='utf-8'))
    except Exception:
        return None


def read_requirements(path: Path):
    p = path / 'requirements.txt'
    if not p.exists():
        return None
    try:
        lines = [l.strip() for l in p.read_text(encoding='utf-8').splitlines() if l.strip() and not l.strip().startswith('#')]
        return lines
    except Exception:
        return None


def suggest_run_commands(path: Path, entrypoints, pkg_json, reqs):
    cmds = []
    if (path / 'run.sh').exists():
        cmds.append('./run.sh')
    if pkg_json:
        if 'scripts' in pkg_json and 'start' in pkg_json['scripts']:
            cmds.append('npm install && npm run start')
        else:
            cmds.append('npm install && npm run dev')
    if reqs is not None:
        # prefer venv inside project
        cmds.append('python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && python main.py')
    for e in entrypoints:
        if e.endswith('.py'):
            cmds.append(f'python {e}')
    return cmds


def snarky_note(name, languages, entrypoints, pkg_json, reqs):
    parts = []
    if not entrypoints:
        parts.append("No obvious entrypoint. Bold choice.")
    if pkg_json:
        parts.append("Node project present. Expect npm hell or a pleasant surprise.")
    if reqs:
        parts.append("Has Python deps. Hope they pinned versions.")
    if 'python' in languages and 'javascript' in languages:
        parts.append("Polyglot chaos detected. Enjoy merging contexts.")
    if not parts:
        parts.append("Can't tell what this does — it's a mystery wrapped in a folder.")

    # build persona-flavored insult
    tone = "" if VOICE['tone']=='gentle' else " (Bardildo: harsh truth incoming)"
    return ' '.join(parts) + tone


def process_folder(path: Path, write: bool = False):
    languages = detect_languages(path)
    readme = read_first_readme(path)
    entrypoints = find_entrypoints(path)
    pkg_json = read_package_json(path)
    reqs = read_requirements(path)
    stats = {
        'name': path.name,
        'path': str(path),
        'languages': languages,
        'entrypoints': entrypoints,
        'package_json': bool(pkg_json),
        'requirements': len(reqs) if reqs else 0,
        'readme_excerpt': '\n'.join(readme) if readme else '',
        'last_modified': datetime.fromtimestamp(max(p.stat().st_mtime for p in path.glob('**/*') if p.exists())).isoformat() if any(path.glob('**/*')) else None,
    }
    run_cmds = suggest_run_commands(path, entrypoints, pkg_json, reqs)
    manifest = {
        'meta': stats,
        'runbook': {
            'commands': run_cmds,
            'env': [],
            'notes': []
        },
        'bard_note': snarky_note(path.name, languages, entrypoints, pkg_json, reqs)
    }

    if write:
        try:
            with (path / 'manifest.json').open('w', encoding='utf-8') as fh:
                json.dump(manifest, fh, indent=2)
            with (path / 'runbook.txt').open('w', encoding='utf-8') as fh:
                fh.write('\n'.join(run_cmds) + '\n\n# Bardilio Note:\n' + manifest['bard_note'])
        except Exception as e:
            print(f'Failed to write manifest for {path}: {e}', file=sys.stderr)
    return manifest


def scan_root(root: Path, write: bool = False):
    results = {}
    for entry in root.iterdir():
        if not entry.is_dir():
            continue
        if entry.name in SKIP_DIRS:
            continue
        manifest = process_folder(entry, write=write)
        results[entry.name] = manifest
    return results


def explain_command(target: str) -> str:
    import shutil, subprocess
    # Try man, then --help, then README lookup
    man = shutil.which('man')
    if man:
        try:
            out = subprocess.check_output(['man', target], stderr=subprocess.STDOUT, timeout=4)
            return out.decode(errors='ignore')[:4000]
        except Exception:
            pass
    # try --help
    try:
        out = subprocess.check_output([target, '--help'], stderr=subprocess.STDOUT, timeout=4)
        return out.decode(errors='ignore')[:4000]
    except Exception:
        pass
    # fallback: look for README in current dir
    p = Path(target)
    if p.exists() and p.is_dir():
        r = read_first_readme(p)
        if r:
            return '\n'.join(r)
    return f"No manual found for '{target}'. Bardildo suggests: read the source or stop asking." 


def main():
    p = argparse.ArgumentParser(prog='bardildo')
    p.add_argument('--root', default='.', help='Root to scan')
    p.add_argument('--write', action='store_true', help='Write manifest.json and runbook.txt into each folder')
    p.add_argument('--headless', action='store_true', help='Print detailed per-folder manifests to stdout as they are written')
    p.add_argument('--alias', action='store_true', help='Print shell alias for easy use')
    p.add_argument('--buddy', choices=['askhole','dustbunny','summarizer','archivist','qa'], help='Invoke a helper persona for quick tasks')
    p.add_argument('--target', help='Target for buddy (e.g., command or folder)')
    args = p.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print('Root not found:', root)
        sys.exit(1)

    if args.alias:
        script = Path(__file__).resolve()
        alias = f"alias bardildo='python3 {script} --root {root} --write --headless'"
        print('# Add this to your shell rc (e.g., ~/.bashrc)')
        print(alias)
        return

    if args.buddy:
        target = args.target or '.'
        buddy = args.buddy
        # run buddy helpers using the local scripts for isolation and Termux-safety
        buddy_script = Path(__file__).parent / f"{buddy}.py"
        if buddy_script.exists():
            import subprocess
            try:
                # If Ollama available and an _ollama variant exists, prefer that
                from ollama_client import list_models
                models = list_models()
            except Exception:
                models = []
            ollama_script = Path(__file__).parent / f"{buddy}_ollama.py"
            script_to_run = None
            if models and ollama_script.exists():
                script_to_run = ollama_script
            else:
                script_to_run = buddy_script
            try:
                # pass persona if provided
                cmd = [sys.executable, str(script_to_run), '--path', str(Path(target).resolve())]
                # allow optional persona flag
                if '--persona' in sys.argv:
                    idx = sys.argv.index('--persona')
                    persona_val = sys.argv[idx+1] if idx+1 < len(sys.argv) else None
                    if persona_val:
                        cmd += ['--persona', persona_val]
                out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=120)
                print(f"\n-- {buddy} output ({'ollama' if script_to_run==ollama_script else 'local'}): --\n")
                print(out.decode(errors='ignore'))
            except subprocess.CalledProcessError as e:
                print(f"{buddy} failed:\n", e.output.decode(errors='ignore'))
            except Exception as e:
                print(f"{buddy} error: {e}")
            return
        else:
            print(f"Buddy script not found: {buddy_script}")
            return

    # run the scanner and optionally write
    for entry in root.iterdir():
        if not entry.is_dir() or entry.name in SKIP_DIRS:
            continue
        manifest = process_folder(entry, write=args.write)
        if args.headless:
            print('\n' + '='*60)
            print(f"Project: {manifest['meta']['name']} — Path: {manifest['meta']['path']}")
            print('- Languages:', manifest['meta']['languages'])
            print('- Entry points:', manifest['meta']['entrypoints'])
            print('- Run commands:')
            for c in manifest['runbook']['commands']:
                print('   ', c)
            print('\n# Bard note:')
            print(manifest['bard_note'])
            print('='*60 + '\n')

    # final summary
    results = scan_root(root, write=args.write)
    print('\nSummary:')
    print(json.dumps({k: v['meta'] for k, v in results.items()}, indent=2))

if __name__ == '__main__':
    main()
