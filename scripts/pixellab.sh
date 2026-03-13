#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$ROOT_DIR/.venv"
ENV_TEMPLATE="$ROOT_DIR/.env.example"
DEFAULT_ENV_FILE="/tmp/localfarmer.env"
ENV_FILE="${LOCALFARMER_ENV_FILE:-$DEFAULT_ENV_FILE}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
PORT="${PORT:-8765}"

usage() {
  cat <<'EOF'
PixelLab installer / upgrader / uninstaller

Usage:
  ./scripts/pixellab.sh install [--env-file PATH]
  ./scripts/pixellab.sh upgrade [--env-file PATH] [--pull]
  ./scripts/pixellab.sh uninstall [--env-file PATH] [--purge-data] [--purge-env]
  ./scripts/pixellab.sh run
  ./scripts/pixellab.sh status

Commands:
  install    Check environment, create .venv, install Python deps, initialize env file.
  upgrade    Reinstall dependencies and optionally git pull --ff-only before upgrading.
  uninstall  Remove .venv and editable install artifacts. Keeps save/logs/env by default.
  run        Start the local FastAPI service on 127.0.0.1:8765.
  status     Print current install and runtime status.

Options:
  --env-file PATH   Use a custom env file instead of /tmp/localfarmer.env.
  --pull            For upgrade: run git pull --ff-only before reinstalling.
  --purge-data      For uninstall: also remove save/ and logs/.
  --purge-env       For uninstall: also remove the selected env file.

Notes:
  - At least one LLM config is required in the env file before meaningful dialogue works.
  - BRAVE_API_KEY is optional. Without it, PixelLab falls back to internal hotspot generation.
EOF
}

log() {
  printf '[pixellab] %s\n' "$*"
}

die() {
  printf '[pixellab] ERROR: %s\n' "$*" >&2
  exit 1
}

parse_common_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --env-file)
        [[ $# -ge 2 ]] || die "--env-file requires a path"
        ENV_FILE="$2"
        shift 2
        ;;
      *)
        break
        ;;
    esac
  done
  REMAINING_ARGS=("$@")
}

check_python() {
  command -v "$PYTHON_BIN" >/dev/null 2>&1 || die "Cannot find $PYTHON_BIN"
  "$PYTHON_BIN" - <<'PY'
import sys
required = (3, 11)
if sys.version_info < required:
    raise SystemExit(f"Python {required[0]}.{required[1]}+ is required, current: {sys.version.split()[0]}")
print(sys.version.split()[0])
PY
}

ensure_git_repo() {
  [[ -d "$ROOT_DIR/.git" ]] || die "This directory is not a git clone: $ROOT_DIR"
}

ensure_env_file() {
  mkdir -p "$(dirname "$ENV_FILE")"
  if [[ ! -f "$ENV_FILE" ]]; then
    cp "$ENV_TEMPLATE" "$ENV_FILE"
    log "Created env file: $ENV_FILE"
  fi
}

ensure_runtime_dirs() {
  mkdir -p "$ROOT_DIR/save" "$ROOT_DIR/logs" "$ROOT_DIR/logs/text_exports"
}

install_python_deps() {
  "$PYTHON_BIN" -m venv "$VENV_DIR"
  # shellcheck disable=SC1091
  source "$VENV_DIR/bin/activate"
  python -m pip install --upgrade pip
  python -m pip install -e "$ROOT_DIR"
}

check_llm_hint() {
  if ! grep -Eq '^(OPENAI_API_KEY|QWEN_API_KEY)=.+' "$ENV_FILE"; then
    log "Env file is initialized, but no OPENAI_API_KEY or QWEN_API_KEY is set yet."
  fi
}

install_cmd() {
  parse_common_args "$@"
  [[ ${#REMAINING_ARGS[@]} -eq 0 ]] || die "Unknown install args: ${REMAINING_ARGS[*]}"
  ensure_git_repo
  log "Checking Python version..."
  check_python >/dev/null
  log "Preparing virtual environment and installing dependencies..."
  install_python_deps
  ensure_runtime_dirs
  ensure_env_file
  check_llm_hint
  cat <<EOF

PixelLab install complete.

Project root: $ROOT_DIR
Virtualenv:    $VENV_DIR
Env file:      $ENV_FILE

Next steps:
  1. Edit the env file and add either OPENAI_API_KEY or QWEN_API_KEY.
  2. Start the app:
     ./scripts/pixellab.sh run
EOF
}

upgrade_cmd() {
  local do_pull=0
  parse_common_args "$@"
  while [[ ${#REMAINING_ARGS[@]} -gt 0 ]]; do
    case "${REMAINING_ARGS[0]}" in
      --pull)
        do_pull=1
        REMAINING_ARGS=("${REMAINING_ARGS[@]:1}")
        ;;
      *)
        die "Unknown upgrade args: ${REMAINING_ARGS[*]}"
        ;;
    esac
  done
  ensure_git_repo
  if [[ $do_pull -eq 1 ]]; then
    if [[ -n "$(git -C "$ROOT_DIR" status --porcelain)" ]]; then
      die "Worktree is dirty; commit or stash changes before --pull"
    fi
    log "Pulling latest changes..."
    git -C "$ROOT_DIR" pull --ff-only
  fi
  log "Checking Python version..."
  check_python >/dev/null
  log "Upgrading local install..."
  install_python_deps
  ensure_runtime_dirs
  ensure_env_file
  check_llm_hint
  log "Upgrade complete."
}

uninstall_cmd() {
  local purge_data=0
  local purge_env=0
  parse_common_args "$@"
  while [[ ${#REMAINING_ARGS[@]} -gt 0 ]]; do
    case "${REMAINING_ARGS[0]}" in
      --purge-data)
        purge_data=1
        REMAINING_ARGS=("${REMAINING_ARGS[@]:1}")
        ;;
      --purge-env)
        purge_env=1
        REMAINING_ARGS=("${REMAINING_ARGS[@]:1}")
        ;;
      *)
        die "Unknown uninstall args: ${REMAINING_ARGS[*]}"
        ;;
    esac
  done

  if command -v lsof >/dev/null 2>&1; then
    local pids
    pids="$(lsof -ti tcp:"$PORT" || true)"
    if [[ -n "$pids" ]]; then
      log "Stopping service on port $PORT..."
      # shellcheck disable=SC2086
      kill $pids || true
    fi
  fi

  rm -rf "$VENV_DIR" "$ROOT_DIR/localfarmer.egg-info" "$ROOT_DIR/__pycache__"
  if [[ $purge_data -eq 1 ]]; then
    rm -rf "$ROOT_DIR/save" "$ROOT_DIR/logs"
  fi
  if [[ $purge_env -eq 1 && -f "$ENV_FILE" ]]; then
    rm -f "$ENV_FILE"
  fi
  log "Uninstall complete."
  if [[ $purge_data -eq 0 ]]; then
    log "Saved data was kept. Use --purge-data if you want to remove save/ and logs/."
  fi
}

run_cmd() {
  [[ -d "$VENV_DIR" ]] || die ".venv not found. Run install first."
  export LOCALFARMER_ENV_FILE="$ENV_FILE"
  # shellcheck disable=SC1091
  source "$VENV_DIR/bin/activate"
  exec python "$ROOT_DIR/run_localfarmer.py"
}

status_cmd() {
  printf 'Project root: %s\n' "$ROOT_DIR"
  printf 'Python:      %s\n' "$(command -v "$PYTHON_BIN" || echo 'not found')"
  printf '.venv:       %s\n' "$( [[ -d "$VENV_DIR" ]] && echo present || echo missing )"
  printf 'Env file:    %s (%s)\n' "$ENV_FILE" "$( [[ -f "$ENV_FILE" ]] && echo present || echo missing )"
  if command -v lsof >/dev/null 2>&1 && lsof -ti tcp:"$PORT" >/dev/null 2>&1; then
    printf 'Service:     running on 127.0.0.1:%s\n' "$PORT"
  else
    printf 'Service:     stopped\n'
  fi
}

main() {
  local command="${1:-}"
  if [[ -z "$command" ]]; then
    usage
    exit 1
  fi
  shift || true
  case "$command" in
    install) install_cmd "$@" ;;
    upgrade) upgrade_cmd "$@" ;;
    uninstall) uninstall_cmd "$@" ;;
    run) run_cmd "$@" ;;
    status) status_cmd "$@" ;;
    -h|--help|help) usage ;;
    *) die "Unknown command: $command" ;;
  esac
}

main "$@"
