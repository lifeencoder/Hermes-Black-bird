#!/usr/bin/env python3
"""
Full deployment script for MoLab:
1. Uploads local notebook.py and custom.css to /marimo/
2. Stops any mock servers on ports 8000 and 8888
3. Ensures hexstrike_server.py is running on port 8888 (with /marimo/hexstrike-ai/venv/bin/python)
4. Ensures vLLM server is running on port 8000 (with NousResearch/Hermes-3-Llama-3.1-70B-FP8)
5. Executes the test prompt via AgentRunner/ModelClient and retrieves the live Linux execution result
"""

import os
import sys
import base64
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from remote_exec import run_code

LOCAL_ROOT = Path(__file__).resolve().parent.parent

with open(LOCAL_ROOT / "notebook.py", "rb") as f:
    nb_b64 = base64.b64encode(f.read()).decode("ascii")

with open(LOCAL_ROOT / "custom.css", "rb") as f:
    css_b64 = base64.b64encode(f.read()).decode("ascii")

remote_deploy_code = f"""
import os
import sys
import time
import socket
import subprocess
import json
import base64

print("=" * 60)
print("🚀 [MoLab] Commencing Phase 2 Deployment")
print("=" * 60)

# 1. Upload files
with open('/marimo/notebook.py', 'wb') as f:
    f.write(base64.b64decode('{nb_b64}'))
print("[✓] /marimo/notebook.py written successfully.")

with open('/marimo/custom.css', 'wb') as f:
    f.write(base64.b64decode('{css_b64}'))
print("[✓] /marimo/custom.css written successfully.")

# Helper: check port
def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2.0)
        return s.connect_ex(('127.0.0.1', port)) == 0

# 2. Kill Mock Servers
print("[*] Checking and stopping mock servers on ports 8000 and 8888...")
subprocess.run("pkill -9 -f mock_vllm_server.py || true", shell=True)
subprocess.run("pkill -9 -f mock_custom_mcp.py || true", shell=True)
subprocess.run("pkill -9 -f benchmark_150_tools_server.py || true", shell=True)

# 3. Check / Start Hexstrike Server on Port 8888
print("[*] Checking HexStrike server on port 8888...")
if is_port_open(8888):
    print("  [✓] Port 8888 is already OPEN and listening.")
else:
    print("  [!] Port 8888 is closed. Starting hexstrike_server.py in background...")
    hex_py = "/marimo/hexstrike-ai/venv/bin/python"
    hex_server = "/marimo/hexstrike-ai/hexstrike_server.py"
    if os.path.exists(hex_py) and os.path.exists(hex_server):
        subprocess.Popen(
            f"nohup {{hex_py}} {{hex_server}} > /marimo/hexstrike_server.log 2>&1 &",
            shell=True
        )
        print("  [*] Launched hexstrike_server. Waiting for port 8888...")
        for _ in range(15):
            time.sleep(1)
            if is_port_open(8888):
                print("  [✓] HexStrike server is UP on port 8888!")
                break
        else:
            print("  [!] Warning: Port 8888 not responding yet. Check /marimo/hexstrike_server.log")
    else:
        print(f"  [!] Missing {{hex_py}} or {{hex_server}}")

# 4. Check / Start vLLM on Port 8000
print("[*] Checking vLLM server on port 8000...")
if is_port_open(8000):
    print("  [✓] Port 8000 is already OPEN and listening.")
else:
    print("  [!] Port 8000 is closed. Launching vLLM server...")
    vllm_cmd = (
        "nohup env VLLM_USE_FLASHINFER_SAMPLER=0 /tmp/uv-venv/bin/python -m vllm.entrypoints.openai.api_server "
        "--model NousResearch/Hermes-3-Llama-3.1-70B-FP8 "
        "--dtype bfloat16 "
        "--max-model-len 32768 "
        "--gpu-memory-utilization 0.90 "
        "--tool-call-parser hermes "
        "--enable-auto-tool-choice "
        "--port 8000 > /marimo/vllm_server.log 2>&1 &"
    )
    subprocess.Popen(vllm_cmd, shell=True)
    print("  [*] vLLM command executed in background. Waiting for endpoint...")
    for i in range(120):
        time.sleep(3)
        if is_port_open(8000):
            print(f"  [✓] vLLM server is READY on port 8000 (after {{(i+1)*3}}s)!")
            break
        if (i + 1) % 10 == 0:
            print(f"  [*] Still waiting for vLLM model to load ({{(i+1)*3}}s)...")

# 5. Live Test via Model & Tools
print("-" * 60)
print("[*] Running live end-to-end execution test...")
test_script = '''
import sys
import os

if "/marimo/model_package" not in sys.path:
    sys.path.insert(0, "/marimo/model_package")

from client.model_client import ModelClient
from tools.registry import ToolRegistry
from tools.mcp_client import MCPClient
from runner.agent_runner import AgentRunner

mcp_path = "/marimo/hexstrike-ai/hexstrike_mcp.py"
hex_venv = "/marimo/hexstrike-ai/venv/bin/python"
py_exec = hex_venv if os.path.exists(hex_venv) else sys.executable

print(f"Connecting to MCP: {{mcp_path}} using {{py_exec}}")
mcp = MCPClient(command=py_exec, args=[mcp_path], startup_timeout=30.0)
mcp.start()

registry = ToolRegistry()
registry.register_mcp_tools(mcp)
tools = registry.get_tools()
print(f"[✓] Discovered {{len(tools)}} tools from HexStrike MCP server.")

client = ModelClient(base_url="http://localhost:8000/v1", model_name="NousResearch/Hermes-3-Llama-3.1-70B-FP8")
runner = AgentRunner(client=client, registry=registry, max_turns=5)

prompt = "با استفاده از ابزار execute_command، دستور whoami را اجرا کن."
print(f"Prompt: {{prompt}}")

result = runner.run(prompt)
print("=" * 60)
print("FINAL REAL EXECUTION RESULT:")
print("=" * 60)
print(result.get("content", result) if isinstance(result, dict) else result)
print("=" * 60)
mcp.stop()
'''

with open('/tmp/test_real_execution.py', 'w', encoding='utf-8') as tf:
    tf.write(test_script)

res = subprocess.run([sys.executable, '/tmp/test_real_execution.py'], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("STDERR:", res.stderr)
"""

if __name__ == "__main__":
    run_code(remote_deploy_code)
