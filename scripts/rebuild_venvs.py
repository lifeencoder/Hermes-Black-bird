import os
import shutil
import subprocess

print(">>> 1. Recreating /marimo/hexstrike-ai/venv...", flush=True)
if os.path.exists("/marimo/hexstrike-ai/venv"):
    shutil.rmtree("/marimo/hexstrike-ai/venv")

subprocess.run(["uv", "venv", "/marimo/hexstrike-ai/venv"], check=True)

print(">>> 2. Installing packages into hexstrike venv...", flush=True)
cmd_hex = [
    "uv", "pip", "install", "--python", "/marimo/hexstrike-ai/venv/bin/python",
    "flask", "requests", "mcp", "psutil", "aiohttp", "beautifulsoup4", "selenium", "mitmproxy"
]
subprocess.run(cmd_hex, check=True)
print("HexStrike venv ready!", flush=True)

print(">>> 3. Setting up /tmp/uv-venv for vLLM...", flush=True)
cmd_vllm = [
    "uv", "pip", "install", "--python", "/tmp/uv-venv/bin/python",
    "vllm==0.32.0"
]
subprocess.run(cmd_vllm, check=True)
print("vLLM installed successfully in /tmp/uv-venv!", flush=True)
