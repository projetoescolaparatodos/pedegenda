#!/usr/bin/env bash
set -euo pipefail

# Render fornece a porta em $PORT
: "${PORT:=8501}"

exec python -m streamlit run app.py \
  --server.address 0.0.0.0 \
  --server.port "$PORT" \
  --server.headless true \
  --browser.gatherUsageStats false
