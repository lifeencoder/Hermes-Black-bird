import subprocess

print('=== GPU STATUS ===')
print(subprocess.getoutput('nvidia-smi --query-gpu=name,memory.total,memory.used,memory.free --format=csv,noheader'))

print('\n=== PROCESSES ON PORTS 8000 & 8888 ===')
print(subprocess.getoutput('ss -tulpn | grep -E "8000|8888"'))

print('\n=== PS AUX VLLM & HEXSTRIKE ===')
print(subprocess.getoutput('ps aux | grep -E "vllm|hexstrike" | grep -v grep'))

print('\n=== VLLM LOG TAIL ===')
print(subprocess.getoutput('tail -n 25 /marimo/vllm_server.log 2>&1'))

print('\n=== CURL TEST 8000 (vLLM Models) ===')
print(subprocess.getoutput('curl -s http://127.0.0.1:8000/v1/models'))

print('\n=== CURL TEST 8888 (Hexstrike Health) ===')
print(subprocess.getoutput('curl -s http://127.0.0.1:8888/health'))
