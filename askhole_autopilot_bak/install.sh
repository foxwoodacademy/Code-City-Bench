#!/bin/sh
set -eu

BASE="/storage/emulated/0/RootBase/askhole_autopilot"
SRC_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

mkdir -p "$BASE/bin" "$BASE/lib" "$BASE/state" "$BASE/webhooks" "$BASE/triggers"

for f in shared.py state_engine.py pipeline.py; do
  cp "$SRC_DIR/lib/$f" "$BASE/lib/$f"
done

for f in askhole-daemon askhole-trigger askhole-status askhole-webhook; do
  cp "$SRC_DIR/bin/$f" "$BASE/bin/$f"
  chmod +x "$BASE/bin/$f"
done

cat > "$BASE/state/README.txt" <<'EOF'
Autopilot state lives here.
EOF

echo "askhole_autopilot installed to $BASE"
