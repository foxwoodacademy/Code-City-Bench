#!/bin/sh
set -eu

API_KEY="${GEMINI_API_KEY:-}"
MODEL="${GEMINI_MODEL:-gemini-2.5-flash-lite}"

if [ -z "$API_KEY" ]; then
  echo "[ERROR] No GEMINI_API_KEY set" >&2
  exit 1
fi

if [ "$#" -eq 0 ]; then
  echo "Usage: gemini <prompt>" >&2
  exit 1
fi

PROMPT="$(printf '%s ' "$@" | sed 's/[[:space:]]\+$//')"
BODY="$(python3 - "$PROMPT" <<'PY'
import json
import sys
prompt = sys.argv[1]
print(json.dumps({"contents":[{"parts":[{"text": prompt}]}]}))
PY
)"

curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$BODY" \
| python3 -c "import json,sys; data=json.load(sys.stdin); print(data['candidates'][0]['content']['parts'][0]['text'])"
