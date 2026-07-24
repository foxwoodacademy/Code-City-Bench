#!/usr/bin/env python3
"""Archivist buddy (stub)
Produces release notes / manifest helpers. Preview-only by default.
"""
import argparse
from pathlib import Path

def manifest_preview(path: Path):
    return { 'name': path.name, 'files': len(list(path.rglob('*'))) }

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--path', default='.')
    args = p.parse_args()
    print(manifest_preview(Path(args.path)))
