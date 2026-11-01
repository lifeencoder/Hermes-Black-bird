import subprocess

print("=== CHECK PSUTIL IN HEXSTRIKE VENV ===")
print(subprocess.getoutput("/marimo/hexstrike-ai/venv/bin/python -c 'import psutil; print(psutil.__file__)'"))
print("\nFiles in psutil dir:")
print(subprocess.getoutput("ls -la /marimo/hexstrike-ai/venv/lib/python3.13/site-packages/psutil/"))
