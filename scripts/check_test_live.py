import subprocess

print("=== CHECKING ACTIVE TEST PROCESS ===")
print(subprocess.getoutput("ps aux | grep -E 'test_persian|vllm' | grep -v grep"))

print("\n=== VLLM LOG (LAST 15 LINES) ===")
print(subprocess.getoutput("tail -n 15 /marimo/vllm_server.log"))
