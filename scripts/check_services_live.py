import subprocess
import os

print("=== 1. PROCESS CHECK ===")
print(subprocess.getoutput("ps aux | grep -E 'hexstrike|vllm' | grep -v grep"))

print("\n=== 2. HEXSTRIKE LOG TAIL ===")
if os.path.exists("/marimo/hexstrike_server.log"):
    print(subprocess.getoutput("tail -n 15 /marimo/hexstrike_server.log"))
else:
    print("hexstrike_server.log not found")

print("\n=== 3. VLLM LOG TAIL ===")
if os.path.exists("/marimo/vllm_server.log"):
    print(subprocess.getoutput("tail -n 15 /marimo/vllm_server.log"))
else:
    print("vllm_server.log not found")

print("\n=== 4. CURL CHECKS ===")
print("HexStrike 8888:", subprocess.getoutput("curl -s http://127.0.0.1:8888/health || echo 'offline'"))
print("vLLM 8000:", subprocess.getoutput("curl -s http://127.0.0.1:8000/v1/models || echo 'offline'"))
