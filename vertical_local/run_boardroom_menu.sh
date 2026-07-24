#!/usr/bin/env bash
# Interactive menu wrapper for run_boardroom.sh
# Run with: bash run_boardroom_menu.sh  (works even if filesystem is mounted noexec)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN="$SCRIPT_DIR/run_boardroom.sh"

if [ ! -f "$RUN" ]; then
  echo "run_boardroom.sh not found in $SCRIPT_DIR"
  exit 1
fi

while true; do
  cat <<MENU

Vertical AI — Boardroom helper
1) Start server
2) Stop server
3) Status / tail log
4) Install deps (pip --user)
5) Populate persona_map
6) Open boardroom URL (prints URL)
7) Exit

Choose an option [1-7]:
MENU

  read -r -p "> " opt
  case "$opt" in
    1) bash "$RUN" start ;;
    2) bash "$RUN" stop || true ;;
    3) bash "$RUN" status || true ;;
    4) bash "$RUN" install-deps || true ;;
    5) bash "$RUN" populate || true ;;
    6)
       HOST="${HOST:-127.0.0.1}"
       PORT="${PORT:-8000}"
       echo "Open in browser: http://$HOST:$PORT/boardroom"
       ;;
    7) echo "Bye"; exit 0 ;;
    *) echo "Invalid choice" ;;
  esac
done
