#!/usr/bin/env python3
"""QA buddy (stub)
Performs quick lint-like checks and test discovery.
"""
import argparse
from pathlib import Path

def qa_preview(path: Path):
    tests = list(path.rglob('test_*.py'))
    return { 'tests_found': len(tests), 'tests': [str(t) for t in tests[:10]] }

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--path', default='.')
    args = p.parse_args()
    print(qa_preview(Path(args.path)))
