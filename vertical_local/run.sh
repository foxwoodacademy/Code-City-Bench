#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
exec uvicorn app:app --host ${HOST:-0.0.0.0} --port ${PORT:-8000} --workers 1
