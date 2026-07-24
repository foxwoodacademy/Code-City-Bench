#!/bin/sh
set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
VENV_CHECK="${PYTHON:-python3}"
VAULT_PATH="${VAULT_PATH:-$HOME/.openclaw/vault.enc}"

usage() {
  cat <<EOF
Usage: install.sh [--seed]

--seed   Initialize an empty encrypted vault at \$VAULT_PATH if VAULT_MASTER_KEY is set.
EOF
}

SEED=0
while [ "$#" -gt 0 ]; do
  case "$1" in
    --seed) SEED=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
  shift
done

"$VENV_CHECK" - <<'PY'
try:
    import cryptography  # noqa: F401
except Exception as exc:
    raise SystemExit(f"cryptography is required: {exc}")
PY

mkdir -p "$HOME/.openclaw"

cat > "$HOME/.openclaw/mediator.env.example" <<EOF
VAULT_MASTER_KEY=change-me
VAULT_PATH=$VAULT_PATH
PYTHONPATH=$ROOT/src
EOF

if [ "$SEED" -eq 1 ]; then
  if [ -z "${VAULT_MASTER_KEY:-}" ]; then
    echo "VAULT_MASTER_KEY is required to seed the vault." >&2
    exit 1
  fi

  ROOT_ENV="$ROOT" "$VENV_CHECK" - "$VAULT_PATH" <<'PY'
import json
import os
import sys

root = os.environ["ROOT_ENV"]
sys.path.insert(0, os.path.join(root, "src"))
from vault import Vault

vault_path = sys.argv[1]
vault = Vault(vault_path)
vault._ensure_path()
with open(vault_path, "wb") as fh:
    fh.write(vault.cipher.encrypt(json.dumps({}).encode()))
print(f"initialized {vault_path}")
PY
fi

echo "mediator setup complete"
