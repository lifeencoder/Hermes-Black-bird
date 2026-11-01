import subprocess

print("=== TESTING HEXSTRIKE SERVER SCRIPT ===")
print(subprocess.getoutput("/marimo/hexstrike-ai/venv/bin/python /marimo/hexstrike-ai/hexstrike_server.py --help"))
