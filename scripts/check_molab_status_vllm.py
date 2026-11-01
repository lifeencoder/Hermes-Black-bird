import subprocess
import os

print("=== CHECKING VLLM & MOUNTS ===")
print("Disk space:")
print(subprocess.getoutput("df -h /marimo"))

print("\nProcess check (vllm, uv):")
print(subprocess.getoutput("ps aux | grep -E 'vllm|uv' | grep -v grep"))

vllm_py = "/marimo/venvs/vllm/bin/python"
if os.path.exists(vllm_py):
    print("\nTesting vllm binary:")
    print(subprocess.getoutput(f"{vllm_py} -c 'import vllm; print(\"vllm version:\", vllm.__version__)'"))
else:
    print(f"\n{vllm_py} does not exist!")

if os.path.exists("/marimo/vllm_install.log"):
    print("\nInstall log tail:")
    print(subprocess.getoutput("tail -n 20 /marimo/vllm_install.log"))
