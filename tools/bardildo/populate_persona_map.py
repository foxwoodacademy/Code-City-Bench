#!/usr/bin/env python3
"""Populate tools/bardildo/persona_map.json from local Ollama models.
Usage:
  python3 populate_persona_map.py --dry-run
  python3 populate_persona_map.py --output /path/to/persona_map.json

Behavior:
- Queries $OLLAMA_URI or http://127.0.0.1:11434/api/tags
- Selects models smaller than 2GB when possible
- Maps detected models to known persona IDs, preserving existing prompt_prefix values when possible
- Writes persona_map.json (overwrite) unless --dry-run
"""

import os
import json
import argparse
try:
    from urllib.request import urlopen, Request
except Exception:
    urlopen = None

DEFAULT_OLLAMA = os.environ.get('OLLAMA_URI', 'http://127.0.0.1:11434')
PERSONA_KEYS = ['askhole','pummelizer','fartographer','adolphin','summarizer','archivist','qa']
DEFAULT_PROMPTS = {
    'askhole': 'You are Askhole, a blunt, snarky CLI helper. Answer concisely with attitude:',
    'pummelizer': 'You are Pummelizer, skeptical and heavy on odds and risk; give skeptical analysis and probabilities:',
    'fartographer': 'You are Fartographer, the roadmap bard. Produce a clear object roadmap and visual steps:',
    'adolphin': 'You are Adolphin, an Austrian dolphin dictator with terrible poetry and blunt commentary; be humorous but actionable:',
    'summarizer': 'You are an executive summarizer:',
    'archivist': 'You are Archivist, produce release notes and changelog bullets:',
    'qa': 'You are QA Buddy, list high-value tests and edge cases:'
}


def fetch_models(ollama_uri):
    url = ollama_uri.rstrip('/') + '/api/tags'
    if urlopen is None:
        raise RuntimeError('urllib not available')
    req = Request(url, headers={'Accept':'application/json'})
    with urlopen(req, timeout=15) as resp:
        data = resp.read().decode('utf-8')
        return json.loads(data)


def pick_models(tags_json, max_size=2_000_000_000):
    candidates = []
    models = tags_json.get('models') if isinstance(tags_json, dict) else tags_json
    if not models:
        return []
    for m in models:
        name = m.get('name') or m.get('model')
        size = m.get('size') or (m.get('details') or {}).get('size')
        try:
            size_int = int(size) if size is not None else 10**12
        except Exception:
            size_int = 10**12
        candidates.append({'name': name, 'size': size_int, 'raw': m})
    # prefer models under max_size
    small = [c for c in candidates if c['size'] < max_size]
    ordered = small + [c for c in candidates if c['size'] >= max_size]
    # unique by name
    seen = set(); uniq = []
    for c in ordered:
        if c['name'] not in seen:
            seen.add(c['name']); uniq.append(c)
    return uniq


def load_existing_map(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--ollama', default=os.environ.get('OLLAMA_URI', DEFAULT_OLLAMA))
    p.add_argument('--output', default=os.path.join(os.path.dirname(__file__), 'persona_map.json'))
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args()

    print('OLLAMA URI:', args.ollama)
    try:
        tags = fetch_models(args.ollama)
    except Exception as e:
        print('Failed to fetch models from Ollama:', e)
        tags = {}

    picked = pick_models(tags)
    print('Detected models (sample):')
    for i,c in enumerate(picked[:10]):
        print(f"  {i+1}. {c['name']} (size={c['size']})")

    existing = load_existing_map(args.output)
    out = {}
    for i,key in enumerate(PERSONA_KEYS):
        prompt_prefix = (existing.get(key) or {}).get('prompt_prefix') or DEFAULT_PROMPTS.get(key)
        model_name = None
        if i < len(picked):
            model_name = picked[i]['name']
        else:
            model_name = (existing.get(key) or {}).get('model') or 'tinyllama:latest'
        out[key] = {'model': model_name, 'prompt_prefix': prompt_prefix}

    print('\nPersona map to write:')
    print(json.dumps(out, indent=2))

    if args.dry_run:
        print('\nDry run — not writing file.')
        return
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(out, f, indent=2)
        print('\nWrote persona_map to', args.output)
    except Exception as e:
        print('Failed to write persona_map.json:', e)


if __name__ == '__main__':
    main()
