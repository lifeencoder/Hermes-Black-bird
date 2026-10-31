import os
import subprocess

start_sh = """#!/bin/bash
export HF_HOME=/marimo/hf_cache
export VLLM_USE_FLASHINFER_SAMPLER=0

echo ">>> Launching HexStrike on port 8888..."
nohup /marimo/hexstrike-ai/venv/bin/python /marimo/hexstrike-ai/hexstrike_server.py \
  --port 8888 > /marimo/hexstrike_server.log 2>&1 < /dev/null &

echo ">>> Launching vLLM on port 8000 with HF_HOME=/marimo/hf_cache..."
nohup /tmp/uv-venv/bin/python -m vllm.entrypoints.openai.api_server \
  --model NousResearch/Hermes-3-Llama-3.1-70B-FP8 \
  --dtype bfloat16 \
  --max-model-len 32768 \
  --gpu-memory-utilization 0.90 \
  --tool-call-parser hermes \
  --enable-auto-tool-choice \
  --port 8000 > /marimo/vllm_server.log 2>&1 < /dev/null &

echo "Services started in background."
"""

with open('/marimo/start_services.sh', 'w') as f:
    f.write(start_sh)

os.chmod('/marimo/start_services.sh', 0o755)

p = subprocess.Popen(
    ['/bin/bash', '/marimo/start_services.sh'],
    start_new_session=True,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    stdin=subprocess.DEVNULL
)
print("Started services script detached with PID:", p.pid)
