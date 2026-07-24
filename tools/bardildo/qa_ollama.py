#!/usr/bin/env python3
"""Ollama-backed QA buddy: suggests tests and edge cases
"""
import argparse
from pathlib import Path
from ollama_client import generate

import json
DEFAULT_MODEL = 'qa-buddy:latest'
PERSONA_MAP = None
try:
    PERSONA_MAP = json.loads(Path(__file__).with_name('persona_map.json').read_text())
except Exception:
    PERSONA_MAP = {}


def qa_suggest(path: Path, model: str | None = None, persona: str | None = None):
    persona_prefix = ''
    model_choice = model or DEFAULT_MODEL
    if persona and persona in PERSONA_MAP:
        persona_prefix = PERSONA_MAP[persona].get('prompt_prefix','') + '\n'
        model_choice = PERSONA_MAP[persona].get('model', model_choice)
    prompt = f"{persona_prefix}You are a senior QA engineer. For the project at {path}, list 10 high-value tests or checks (unit/integration/security/perf), and give one-line instructions to implement each. Prioritize quick wins."
    return generate(prompt, model_choice)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--path', default='.')
    p.add_argument('--model', default=None)
    p.add_argument('--persona', default=None)
    args = p.parse_args()
    print(qa_suggest(Path(args.path), args.model, args.persona))
