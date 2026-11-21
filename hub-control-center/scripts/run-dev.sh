#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT/app"
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
exec uvicorn hub.main:app --host 127.0.0.1 --port 8787 --reload
