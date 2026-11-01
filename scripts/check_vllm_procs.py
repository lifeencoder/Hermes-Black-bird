import subprocess

print("=== CHECKING VLLM PROCESSES ===")
print(subprocess.getoutput("ps aux | grep -E 'vllm|27492|28290' | grep -v grep"))
