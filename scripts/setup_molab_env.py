import os
import subprocess

print(">>> 1. Creating directories...", flush=True)
os.makedirs("/marimo/hf_cache", exist_ok=True)
os.makedirs("/marimo/model_package", exist_ok=True)

print(">>> 2. Setting up hexstrike-ai venv...", flush=True)
subprocess.run(["uv", "venv", "/marimo/hexstrike-ai/venv", "--allow-existing"], check=True)

print(">>> 3. Installing dependencies into hexstrike-ai venv...", flush=True)
cmd_hex = [
    "uv", "pip", "install", "--python", "/marimo/hexstrike-ai/venv/bin/python",
    "flask", "requests", "mcp", "psutil", "aiohttp", "beautifulsoup4", "selenium", "mitmproxy"
]
subprocess.run(cmd_hex, check=True)
print("hexstrike-ai venv setup COMPLETE!", flush=True)

print(">>> 4. Installing vLLM into /tmp/uv-venv...", flush=True)
cmd_vllm = [
    "uv", "pip", "install", "--python", "/tmp/uv-venv/bin/python",
    "vllm==0.32.0"
]
subprocess.run(cmd_vllm, check=True)
print("vLLM installation COMPLETE!", flush=True)
