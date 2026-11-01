import subprocess

print("=== GPU & CPU STATUS ===")
print(subprocess.getoutput("nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv"))
print("\n=== TOP PROCESSES ===")
print(subprocess.getoutput("ps aux | grep -E 'python|vllm' | grep -v grep | head -n 10"))
