import subprocess

print("=== CHECKING VLLM VENV ===")
print("vLLM output:", subprocess.getoutput("/tmp/uv-venv/bin/python -c 'import vllm; print(vllm.__version__)'"))

print("\n=== CHECKING HEXSTRIKE VENV ===")
print("HexStrike output:", subprocess.getoutput("/marimo/hexstrike-ai/venv/bin/python -c 'import flask, mcp, requests; print(\"HexStrike imports OK\")'"))

print("\n=== RUNNING PROCESSES ===")
print(subprocess.getoutput("ps aux | grep -E 'vllm|hexstrike' | grep -v grep"))

print("\n=== PORT 8000 & 8888 ===")
print("Port 8000:", subprocess.getoutput("curl -s http://127.0.0.1:8000/v1/models || echo 'Down'"))
print("Port 8888:", subprocess.getoutput("curl -s http://127.0.0.1:8888/health || echo 'Down'"))
