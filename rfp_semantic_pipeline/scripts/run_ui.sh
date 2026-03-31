#!/usr/bin/env bash
set -euo pipefail
streamlit run app/ui/streamlit_app.py --server.port ${STREAMLIT_PORT:-8501}
