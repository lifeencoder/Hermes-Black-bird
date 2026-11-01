import subprocess

print("=== VLLM AUTO RECOVER LOG ===")
print(subprocess.getoutput("cat /marimo/vllm_auto_recover.log"))

print("\n=== HEXSTRIKE AUTO RECOVER LOG ===")
print(subprocess.getoutput("cat /marimo/hexstrike_auto_recover.log"))
