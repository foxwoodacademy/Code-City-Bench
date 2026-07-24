#!/usr/bin/env python3
"""Ollama-backed Summarizer buddy
"""
import argparse
from pathlib import Path
from ollama_client import generate

import json
DEFAULT_MODEL = 'summarizer:latest'

PERSONA_MAP = None
try:
    PERSONA_MAP = json.loads(Path(__file__).with_name('persona_map.json').read_text())
except Exception:
    PERSONA_MAP = {}


def summarize(path: Path, model: str | None = None, persona: str | None = None):
    files = list(path.rglob('*'))[:200]
    sample = '\n'.join([str(f) for f in files[:20]])
    persona_prefix = ''
    model_choice = model or DEFAULT_MODEL
    if persona and persona in PERSONA_MAP:
        persona_prefix = PERSONA_MAP[persona].get('prompt_prefix','') + '\n'
        model_choice = PERSONA_MAP[persona].get('model', model_choice)
    prompt = f"{persona_prefix}You are an executive summarizer. Produce a concise (3-paragraph max) executive summary for the project at {path}. List key entrypoints and a 3-step recommended action plan. Files sample:\n{sample}"
    return generate(prompt, model_choice)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--path', default='.')
    p.add_argument('--model', default=None)
    p.add_argument('--persona', default=None)
    args = p.parse_args()
    print(summarize(Path(args.path), args.model, args.persona))
