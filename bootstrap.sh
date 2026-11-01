#!/usr/bin/env bash
# ==============================================================================
# Hermes Black Bird - Automated Bootstrap & Environment Restorer (bootstrap.sh)
# One-touch script to ensure persistent venvs and services are 100% operational.
# ==============================================================================
set -e

MARIMO_DIR="/marimo"
VLLM_VENV="$MARIMO_DIR/venvs/vllm"
HEX_VENV="$MARIMO_DIR/hexstrike-ai/venv"
HF_CACHE="$MARIMO_DIR/hf_cache"

mkdir -p "$MARIMO_DIR/venvs" "$HF_CACHE"

echo "=================================================="
echo "🦅 Hermes Black Bird - Bootstrap & Health Check"
echo "=================================================="

# 1. HexStrike venv check
if [ ! -f "$HEX_VENV/bin/python" ]; then
    echo "[1/3] Creating HexStrike virtualenv at $HEX_VENV..."
    uv venv "$HEX_VENV"
    echo "      Installing HexStrike dependencies..."
    uv pip install --python "$HEX_VENV/bin/python" flask requests mcp psutil
else
    echo "[1/3] HexStrike virtualenv exists."
    # Ensure psutil is healthy
    if ! "$HEX_VENV/bin/python" -c "import psutil" > /dev/null 2>&1; then
        echo "      Fixing psutil in HexStrike venv..."
        uv pip install --reinstall psutil --python "$HEX_VENV/bin/python"
    fi
fi

# 2. vLLM persistent venv check
if [ ! -f "$VLLM_VENV/bin/python" ]; then
    echo "[2/3] Creating vLLM virtualenv at $VLLM_VENV..."
    uv venv "$VLLM_VENV"
    echo "      Installing vLLM into persistent venv (this takes ~1-2 min)..."
    uv pip install vllm --python "$VLLM_VENV/bin/python"
else
    echo "[2/3] vLLM persistent virtualenv exists."
    if ! "$VLLM_VENV/bin/python" -c "import vllm" > /dev/null 2>&1; then
        echo "      Installing missing vLLM packages..."
        uv pip install vllm --python "$VLLM_VENV/bin/python"
    fi
fi

# 3. Launch Services
echo "[3/3] Invoking start.sh to launch services..."
if [ -f "$MARIMO_DIR/start.sh" ]; then
    bash "$MARIMO_DIR/start.sh"
elif [ -f "./start.sh" ]; then
    bash "./start.sh"
else
    echo "start.sh not found, launching directly..."
    export HF_HOME="$HF_CACHE"
    export VLLM_USE_FLASHINFER_SAMPLER=0
    nohup "$HEX_VENV/bin/python" "$MARIMO_DIR/hexstrike-ai/hexstrike_server.py" --port 8888 > "$MARIMO_DIR/hexstrike_server.log" 2>&1 < /dev/null &
    nohup "$VLLM_VENV/bin/python" -m vllm.entrypoints.openai.api_server \
        --model NousResearch/Hermes-3-Llama-3.1-70B-FP8 \
        --dtype bfloat16 \
        --max-model-len 32768 \
        --gpu-memory-utilization 0.90 \
        --tool-call-parser hermes \
        --enable-auto-tool-choice \
        --port 8000 > "$MARIMO_DIR/vllm_server.log" 2>&1 < /dev/null &
fi

echo "=================================================="
echo "🦅 Bootstrap complete!"
echo "=================================================="
