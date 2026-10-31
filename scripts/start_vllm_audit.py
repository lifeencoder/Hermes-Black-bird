#!/usr/bin/env python3
"""
Start stable Hermes-3 vLLM server on MoLab with nohup and monitor until ready.
"""
import time
import os
import subprocess
import urllib.request
import json

LOG_PATH = "/marimo/vllm_final_audit.log"
PORT = 8000
MODEL_NAME = "NousResearch/Hermes-3-Llama-3.1-70B-FP8"

print("=== STEP 3: Launching Hermes-3 vLLM Server (Detached Background) ===")

# Kill any existing vllm process
subprocess.run(["pkill", "-9", "-f", "vllm"], capture_output=True)
time.sleep(2)

cmd = (
    f"nohup env VLLM_USE_FLASHINFER_SAMPLER=0 /tmp/uv-venv/bin/python -m vllm.entrypoints.openai.api_server "
    f"--model {MODEL_NAME} "
    f"--dtype bfloat16 "
    f"--max-model-len 32768 "
    f"--gpu-memory-utilization 0.90 "
    f"--tool-call-parser hermes "
    f"--enable-auto-tool-choice "
    f"--port {PORT} > {LOG_PATH} 2>&1 &"
)

print(f"Executing: {cmd}")
subprocess.run(cmd, shell=True)
print(f"[✓] vLLM server launched in background. Monitoring {LOG_PATH}...")

start_time = time.time()
max_wait = 360  # 6 minutes
is_ready = False

while time.time() - start_time < max_wait:
    elapsed = int(time.time() - start_time)
    
    try:
        req = urllib.request.Request(f"http://localhost:{PORT}/v1/models")
        with urllib.request.urlopen(req, timeout=3) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                models = [m.get("id") for m in data.get("data", [])]
                print(f"\n[✓] vLLM server is READY! (elapsed: {elapsed}s)")
                print(f"    Status: 200 OK")
                print(f"    Available models: {models}")
                is_ready = True
                break
    except Exception:
        pass
        
    if elapsed % 15 == 0 and elapsed > 0:
        log_snippet = ""
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r", encoding="utf-8", errors="ignore") as lf:
                lines = lf.readlines()
                log_snippet = "".join(lines[-4:])
        print(f"[{elapsed}s] Server initializing... Recent log:\n{log_snippet.strip()}")
        
    time.sleep(3)

if not is_ready:
    print(f"\n[!] Final log check from {LOG_PATH}:")
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8", errors="ignore") as lf:
            lines = lf.readlines()
            print("".join(lines[-35:]))
    raise SystemExit(1)
else:
    print("[✓] Step 3 completed successfully!")
