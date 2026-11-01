import subprocess

print("Python version of vllm venv:")
print(subprocess.getoutput("/marimo/venvs/vllm/bin/python -V"))

print("\nSystem pythons available:")
print(subprocess.getoutput("which python; which python3; which python3.12; which python3.11; which python3.10"))
