#!/bin/zsh
set -euo pipefail
cd /Volumes/Yaoy/project/LocalFarmer
mkdir -p logs
exec ./.venv/bin/python run_localfarmer.py >> logs/server.log 2>&1
