import subprocess

print("=== REINSTALLING PSUTIL IN HEXSTRIKE VENV ===")
print(subprocess.getoutput("uv pip install --reinstall psutil --python /marimo/hexstrike-ai/venv/bin/python"))

print("\nTesting psutil import:")
print(subprocess.getoutput("/marimo/hexstrike-ai/venv/bin/python -c 'import psutil; print(\"psutil ok! version:\", psutil.__version__)'"))
