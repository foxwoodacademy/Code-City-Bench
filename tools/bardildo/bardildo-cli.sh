#!/usr/bin/env bash
# Thin wrapper for bardildo for easy aliasing
ROOT=${1:-/storage/emulated/0/RootBase}
python3 "$ROOT/tools/bardildo/bardildo.py" --root "$ROOT" --write --headless "$@"
