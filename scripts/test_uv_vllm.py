import subprocess

print("=== RESOLVING VLLM ===")
print(subprocess.getoutput("uv pip install --dry-run vllm"))
