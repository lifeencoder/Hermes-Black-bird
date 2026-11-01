import os
import subprocess
import time

script_content = """#!/bin/bash
echo "=== Starting vLLM installation at $(date) ===" > /marimo/vllm_install.log
uv pip install vllm --python /marimo/venvs/vllm/bin/python >> /marimo/vllm_install.log 2>&1
EXIT_CODE=$?
echo "=== vLLM installation finished with code $EXIT_CODE at $(date) ===" >> /marimo/vllm_install.log
"""

with open("/marimo/install_vllm_bg.sh", "w") as f:
    f.write(script_content)

os.chmod("/marimo/install_vllm_bg.sh", 0o755)

# Launch detached
p = subprocess.Popen(
    ["/bin/bash", "/marimo/install_vllm_bg.sh"],
    start_new_session=True,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    stdin=subprocess.DEVNULL
)

print(f"Launched vLLM installation in background PID: {p.pid}")
