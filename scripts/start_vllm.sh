#!/usr/bin/env bash
set -e

# ==============================================================================
# Hermes Black Bird - vLLM Server Startup Script
# Model: NousResearch/Hermes-3-Llama-3.1-70B-FP8
# Port: 8000 (OpenAI Compatible API)
# ==============================================================================

# مسیر کش HuggingFace را در صورت نیاز تغییر دهید
export HF_HOME="${HF_HOME:-/marimo/hf_cache}"
MODEL_NAME="NousResearch/Hermes-3-Llama-3.1-70B-FP8"
PORT=8000
LOG_FILE="vllm_server.log"

echo "=================================================="
echo " Starting Hermes Black Bird vLLM Server"
echo " Model:    $MODEL_NAME"
echo " Port:     $PORT"
echo " HF_HOME:  $HF_HOME"
echo " Logs:     $LOG_FILE"
echo "=================================================="

nohup python -m vllm.entrypoints.openai.api_server \
  --model "$MODEL_NAME" \
  --dtype bfloat16 \
  --max-model-len 32768 \
  --gpu-memory-utilization 0.90 \
  --tool-call-parser hermes \
  --enable-auto-tool-choice \
  --port "$PORT" \
  > "$LOG_FILE" 2>&1 &

PID=$!
echo "$PID" > vllm.pid
echo "vLLM server started in background (PID: $PID)"
echo "Waiting for endpoint to become ready..."

# Healthcheck loop
for i in {1..60}; do
  if curl -s "http://localhost:$PORT/v1/models" > /dev/null 2>&1; then
    echo "vLLM server is READY and responding on http://localhost:$PORT/v1"
    exit 0
  fi
  sleep 2
done

echo "Server is still initializing. Check logs with: tail -f $LOG_FILE"
