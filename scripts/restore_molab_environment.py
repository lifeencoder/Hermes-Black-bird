import os
import sys
import time
import subprocess
from pathlib import Path

# Add scripts directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from remote_exec import run_code, _load_env
from safe_upload_files import upload_file_chunked

def restore_environment():
    _load_env()
    print("=== STEP 1: CLEANING UP PREVIOUS PROCESSES ===")
    cleanup_code = """
import subprocess
print('Killing previous vllm & hexstrike processes...')
subprocess.run(['pkill', '-9', '-f', 'vllm'])
subprocess.run(['pkill', '-9', '-f', 'hexstrike'])
print('Killed existing processes.')
"""
    run_code(cleanup_code)

    print("\n=== STEP 2: SYNCING CLEAN FILES ===")
    root = Path(__file__).resolve().parent.parent
    upload_file_chunked(root / "notebook.py", "/marimo/notebook.py")
    upload_file_chunked(root / "custom.css", "/marimo/custom.css")
    
    # Sync model package files
    for folder in ["client", "runner", "tools", "config"]:
        src_dir = root / folder
        if src_dir.exists():
            for f in src_dir.glob("*.py"):
                upload_file_chunked(f, f"/marimo/model_package/{folder}/{f.name}")
            for f in src_dir.glob("*.yaml"):
                upload_file_chunked(f, f"/marimo/model_package/{folder}/{f.name}")

    print("\n=== STEP 3: CHECKING VIRTUAL ENV & HF_CACHE ===")
    check_code = """
import os
from pathlib import Path

venv_py = Path('/marimo/hexstrike-ai/venv/bin/python')
print('HexStrike venv exists:', venv_py.exists())

hf_cache = Path('/marimo/hf_cache')
print('HF_CACHE (/marimo/hf_cache) exists:', hf_cache.exists())
if hf_cache.exists():
    print('HF_CACHE contents:', os.listdir(str(hf_cache)))

# Also check default cache
home_cache = Path('/home/marimo/.cache/huggingface/hub')
if home_cache.exists():
    print('Home HF cache exists:', os.listdir(str(home_cache)))
"""
    run_code(check_code)

    print("\n=== STEP 4: STARTING REAL SERVICES ===")
    start_code = """
import os
import subprocess

start_sh = '''#!/bin/bash
export HF_HOME=/marimo/hf_cache
export VLLM_USE_FLASHINFER_SAMPLER=0

# Start vLLM on port 8000
nohup /tmp/uv-venv/bin/python -m vllm.entrypoints.openai.api_server \\
  --model NousResearch/Hermes-3-Llama-3.1-70B-FP8 \\
  --dtype bfloat16 \\
  --max-model-len 32768 \\
  --gpu-memory-utilization 0.90 \\
  --tool-call-parser hermes \\
  --enable-auto-tool-choice \\
  --port 8000 > /marimo/vllm_server.log 2>&1 < /dev/null &

# Start HexStrike on port 8888
nohup /marimo/hexstrike-ai/venv/bin/python /marimo/hexstrike-ai/hexstrike_server.py \\
  --port 8888 > /marimo/hexstrike_server.log 2>&1 < /dev/null &
'''

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
print('Started services script detached with PID:', p.pid)
"""
    run_code(start_code)

    print("\n=== STEP 5: APPLYING LIVE UI CELLS ===")
    from apply_live_cells import *
    # apply_live_cells logic
    print("Environment restoration initiated!")

if __name__ == "__main__":
    restore_environment()
