import os
import subprocess
from pathlib import Path

print("=== SETTING UP PERSISTENT VLLM VENV ===")
vllm_venv = Path("/marimo/venvs/vllm")
os.makedirs("/marimo/venvs", exist_ok=True)
os.makedirs("/marimo/hf_cache", exist_ok=True)

vllm_py = vllm_venv / "bin" / "python"
if not vllm_py.exists():
    print(f"Creating venv at {vllm_venv}...")
    print(subprocess.getoutput(f"uv venv {vllm_venv}"))

print("Testing vLLM import in venv...")
test_out = subprocess.getoutput(f"{vllm_py} -c 'import vllm; print(vllm.__version__)'")
if "ModuleNotFoundError" in test_out or "No module named" in test_out:
    print("Installing vllm==0.32.0 into persistent venv...")
    cmd = f"uv pip install vllm==0.32.0 --python {vllm_py}"
    print("Running:", cmd)
    out = subprocess.getoutput(cmd)
    print(out[-500:] if len(out) > 500 else out)

print("\nFinal verification:")
print("vLLM version:", subprocess.getoutput(f"{vllm_py} -c 'import vllm; print(vllm.__version__)'"))
