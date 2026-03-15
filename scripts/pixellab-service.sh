#!/bin/zsh
set -euo pipefail
SESSION="pixellab-server"
ROOT="/Volumes/Yaoy/project/LocalFarmer"
LOG="$ROOT/logs/server.log"
PIDFILE="$ROOT/logs/server.pid"
mkdir -p "$ROOT/logs"
case "${1:-}" in
  start)
    /usr/bin/screen -S "$SESSION" -X quit >/dev/null 2>&1 || true
    /usr/bin/screen -dmS "$SESSION" /bin/zsh -lc "cd '$ROOT' && exec ./.venv/bin/python run_localfarmer.py >> '$LOG' 2>&1"
    sleep 3
    pgrep -f "run_localfarmer.py" | head -n1 > "$PIDFILE" || true
    ;;
  stop)
    /usr/bin/screen -S "$SESSION" -X quit >/dev/null 2>&1 || true
    rm -f "$PIDFILE"
    ;;
  status)
    if /usr/bin/screen -list | grep -q "$SESSION"; then
      echo "running"
      pgrep -f "run_localfarmer.py" | head -n1 || true
    elif lsof -nP -iTCP:8765 -sTCP:LISTEN >/dev/null 2>&1; then
      echo "running"
      lsof -nP -iTCP:8765 -sTCP:LISTEN | awk 'NR==2{print $2}'
    else
      echo "stopped"
      exit 1
    fi
    ;;
  *)
    echo "usage: $0 {start|stop|status}" >&2
    exit 2
    ;;
esac
