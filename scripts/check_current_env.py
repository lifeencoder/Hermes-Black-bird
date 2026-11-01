import subprocess
import sys

print("Current Python:", sys.executable)
print("\nInstalled packages in current python:")
print(subprocess.getoutput("pip list | grep -E 'vllm|torch|marimo|mcp|hexstrike|transformers'"))
