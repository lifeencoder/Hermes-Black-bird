#!/usr/bin/env bash
# ==============================================================================
# Hermes Black Bird - Service Runner (start.sh)
# Starts HexStrike (8888) and vLLM (8000)
# ==============================================================================
set -e

MARIMO_DIR="/marimo"
VLLM_VENV="$MARIMO_DIR/venvs/vllm"
HEX_VENV="$MARIMO_DIR/hexstrike-ai/venv"
HF_CACHE="$MARIMO_DIR/hf_cache"

mkdir -p "$HF_CACHE"

echo "=================================================="
echo "🦅 Hermes Black Bird - Starting Services"
echo "=================================================="

# 1. HexStrike API Server (Port 8888)
echo -n "[1/2] Checking HexStrike on port 8888... "
if curl -s http://127.0.0.1:8888/health > /dev/null 2>&1 || curl -s http://127.0.0.1:8888/ > /dev/null 2>&1; then
    echo "ALREADY RUNNING."
else
    echo "STARTING..."
    nohup "$HEX_VENV/bin/python" "$MARIMO_DIR/hexstrike-ai/hexstrike_server.py" \
        --port 8888 > "$MARIMO_DIR/hexstrike_server.log" 2>&1 < /dev/null &
    HEX_PID=$!
    echo "      HexStrike launched in background (PID: $HEX_PID)"
fi

# 2. vLLM Server (Port 8000)
echo -n "[2/2] Checking vLLM on port 8000... "
if curl -s http://127.0.0.1:8000/v1/models > /dev/null 2>&1; then
    echo "ALREADY RUNNING."
else
    echo "STARTING..."
    export HF_HOME="$HF_CACHE"
    export VLLM_USE_FLASHINFER_SAMPLER=0
    nohup "$VLLM_VENV/bin/python" -m vllm.entrypoints.openai.api_server \
        --model NousResearch/Hermes-3-Llama-3.1-70B-FP8 \
        --dtype bfloat16 \
        --max-model-len 32768 \
        --gpu-memory-utilization 0.90 \
        --tool-call-parser hermes \
        --enable-auto-tool-choice \
        --port 8000 > "$MARIMO_DIR/vllm_server.log" 2>&1 < /dev/null &
    VLLM_PID=$!
    echo "      vLLM launched in background (PID: $VLLM_PID)"
fi

echo "=================================================="
echo "Status check (waiting 3s)..."
sleep 3

if curl -s http://127.0.0.1:8888/health > /dev/null 2>&1 || curl -s http://127.0.0.1:8888/ > /dev/null 2>&1; then
    echo "✅ HexStrike: ONLINE (http://127.0.0.1:8888)"
else
    echo "⏳ HexStrike: INITIALIZING (check /marimo/hexstrike_server.log)"
fi

if curl -s http://127.0.0.1:8000/v1/models > /dev/null 2>&1; then
    echo "✅ vLLM: ONLINE (http://127.0.0.1:8000/v1)"
else
    echo "⏳ vLLM: INITIALIZING / DOWNLOADING WEIGHTS (check /marimo/vllm_server.log)"
fi
echo "=================================================="
