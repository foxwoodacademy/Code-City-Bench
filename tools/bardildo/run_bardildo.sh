#!/usr/bin/env bash
set -euo pipefail
ROOT=${1:-/storage/emulated/0/RootBase}
python3 "$ROOT/tools/bardildo/bardildo.py" --root "$ROOT" --write

echo "Bardildo scan completed. Manifests written where applicable." 
