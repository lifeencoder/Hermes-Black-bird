import subprocess
import os

print("=== CHECKING INSTALL PROCESS ===")
print("Process check:")
print(subprocess.getoutput("ps aux | grep -E 'install_vllm|uv pip' | grep -v grep"))

print("\nLog tail (last 25 lines):")
if os.path.exists("/marimo/vllm_install.log"):
    print(subprocess.getoutput("tail -n 25 /marimo/vllm_install.log"))
else:
    print("Log file does not exist yet.")
