import os
import subprocess
from pathlib import Path

print("=== CHECKING /marimo DIRECTORY ===")
if os.path.exists('/marimo'):
    print("/marimo contents:", os.listdir('/marimo'))
else:
    print("/marimo DOES NOT EXIST!")

print("\n=== CHECKING VIRTUAL ENVS ===")
for p in ['/marimo/hexstrike-ai/venv', '/marimo/venvs', '/tmp/uv-venv']:
    print(f"{p} exists:", os.path.exists(p))

print("\n=== CHECKING HF_CACHE ===")
for p in ['/marimo/hf_cache', '/home/marimo/.cache/huggingface/hub', '/root/.cache/huggingface']:
    print(f"{p} exists:", os.path.exists(p))

print("\n=== CHECKING GPU ===")
print(subprocess.getoutput("nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv,noheader"))
