import subprocess
import os

print("=== PERSIAN TEST OUTPUT ===")
if os.path.exists("/marimo/persian_test_output.txt"):
    content = subprocess.getoutput("cat /marimo/persian_test_output.txt")
    print(content)
else:
    print("File not found")

print("\n=== PROCESS CHECK ===")
print(subprocess.getoutput("ps aux | grep -E 'run_eval_script|32688' | grep -v grep"))
