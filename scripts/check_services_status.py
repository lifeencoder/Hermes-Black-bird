import subprocess

print("=== CHECKING SERVICES STATUS ===")
print("1. HexStrike (8888):")
print(subprocess.getoutput("curl -s http://127.0.0.1:8888/health || curl -s http://127.0.0.1:8888/"))

print("\n2. vLLM (8000):")
print(subprocess.getoutput("curl -s http://127.0.0.1:8000/v1/models"))

print("\n3. Processes:")
print(subprocess.getoutput("ps -ef | grep -E 'python|vllm|hexstrike' | grep -v grep"))

print("\n4. vLLM log tail:")
print(subprocess.getoutput("tail -n 25 /marimo/vllm_server.log"))
