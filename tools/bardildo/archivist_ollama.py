#!/usr/bin/env python3
"""Ollama-backed Archivist buddy: creates release notes / changelog drafts
"""
import argparse
from pathlib import Path
from ollama_client import generate

import json
DEFAULT_MODEL = 'archivist:latest'
PERSONA_MAP = None
try:
    PERSONA_MAP = json.loads(Path(__file__).with_name('persona_map.json').read_text())
except Exception:
    PERSONA_MAP = {}


def manifest(path: Path, model: str | None = None, persona: str | None = None):
    persona_prefix = ''
    model_choice = model or DEFAULT_MODEL
    if persona and persona in PERSONA_MAP:
        persona_prefix = PERSONA_MAP[persona].get('prompt_prefix','') + '\n'
        model_choice = PERSONA_MAP[persona].get('model', model_choice)
    prompt = f"{persona_prefix}You are an archivist. Produce release notes for the project at {path}. Include: 1) summary of recent changes 2) risk notes 3) recommended version tag and changelog bullets (max 10). If files mention 'TODO' include them."
    return generate(prompt, model_choice)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--path', default='.')
    p.add_argument('--model', default=None)
    p.add_argument('--persona', default=None)
    args = p.parse_args()
    print(manifest(Path(args.path), args.model, args.persona))
