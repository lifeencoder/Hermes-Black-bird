import os
import subprocess
from pathlib import Path

print("=== CHECKING /marimo DIRECTORY ===")
if os.path.exists('/marimo'):
    print("/marimo contents:", os.listdir('/marimo'))
else:
    print("/marimo DOES NOT EXIST!")

print("\n=== CHECKING VIRTUAL ENV ===")
venv_path = Path('/marimo/hexstrike-ai/venv')
print(f"venv_path {venv_path} exists:", venv_path.exists())
if venv_path.exists():
    venv_py = venv_path / "bin" / "python"
    print(f"venv python {venv_py} exists:", venv_py.exists())
    if venv_py.exists():
        print("venv python version:", subprocess.getoutput(f"{venv_py} --version"))
        print("testing flask/mcp import in venv:", subprocess.getoutput(f"{venv_py} -c 'import flask, mcp, requests; print(\"Imports OK\")'"))

print("\n=== CHECKING HF_CACHE ===")
hf_cache = Path('/marimo/hf_cache')
print(f"hf_cache {hf_cache} exists:", hf_cache.exists())
if hf_cache.exists():
    print("hf_cache contents:", os.listdir(str(hf_cache)))

# Check other possible cache locations
home_cache = Path('/home/marimo/.cache/huggingface/hub')
print(f"home_cache {home_cache} exists:", home_cache.exists())
if home_cache.exists():
    print("home_cache contents:", os.listdir(str(home_cache)))

print("\n=== CHECKING UV-VENV (vLLM) ===")
uv_venv_py = Path('/tmp/uv-venv/bin/python')
print(f"uv_venv_py {uv_venv_py} exists:", uv_venv_py.exists())
if uv_venv_py.exists():
    print("vllm version:", subprocess.getoutput(f"{uv_venv_py} -c 'import vllm; print(vllm.__version__)'"))

print("\n=== GPU CHECK ===")
print(subprocess.getoutput("nvidia-smi --query-gpu=name,memory.total,memory.used,memory.free --format=csv,noheader"))
