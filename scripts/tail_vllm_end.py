import subprocess

print("=== VLLM LOG END ===")
print(subprocess.getoutput("tail -n 40 /marimo/vllm_server.log"))
