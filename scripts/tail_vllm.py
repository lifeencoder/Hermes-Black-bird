import subprocess

print("=== VLLM LOG (LAST 30 LINES) ===")
print(subprocess.getoutput("tail -n 30 /marimo/vllm_server.log"))
