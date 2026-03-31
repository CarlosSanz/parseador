#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SCRIPT_DIR"
uvicorn app.api.main:app --host ${API_HOST:-127.0.0.1} --port ${API_PORT:-8000} --reload
