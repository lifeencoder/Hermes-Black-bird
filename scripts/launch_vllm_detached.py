import subprocess
import os

script_content = """#!/bin/bash
export VLLM_USE_FLASHINFER_SAMPLER=0
nohup /tmp/uv-venv/bin/python -m vllm.entrypoints.openai.api_server \\
  --model NousResearch/Hermes-3-Llama-3.1-70B-FP8 \\
  --dtype bfloat16 \\
  --max-model-len 32768 \\
  --gpu-memory-utilization 0.90 \\
  --tool-call-parser hermes \\
  --enable-auto-tool-choice \\
  --port 8000 > /marimo/vllm_server.log 2>&1 < /dev/null &
"""

with open('/marimo/start_vllm_daemon.sh', 'w') as f:
    f.write(script_content)

os.chmod('/marimo/start_vllm_daemon.sh', 0o755)

# Launch it completely detached using subprocess.Popen with start_new_session=True
p = subprocess.Popen(
    ['/bin/bash', '/marimo/start_vllm_daemon.sh'],
    start_new_session=True,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    stdin=subprocess.DEVNULL
)
print("Launched start_vllm_daemon.sh with PID:", p.pid)
