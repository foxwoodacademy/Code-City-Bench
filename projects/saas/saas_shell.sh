#!/bin/sh
set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PACKAGES_DIR="$ROOT/saas_packages"

if [ ! -d "$PACKAGES_DIR" ]; then
  echo "package directory not found: $PACKAGES_DIR" >&2
  exit 1
fi

count="$(find "$PACKAGES_DIR" -maxdepth 1 -name '*.json' | wc -l | tr -d ' ')"
echo "saas_packages: $count package file(s)"
python3 "$ROOT/front_desk_lady.py" --packages-dir "$PACKAGES_DIR" --dry-run "$@"
