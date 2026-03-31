#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SCRIPT_DIR"
streamlit run app/ui/streamlit_app.py --server.port ${STREAMLIT_PORT:-8501}
