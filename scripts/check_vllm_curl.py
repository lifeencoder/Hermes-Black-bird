import subprocess

print("=== CHECKING PORT 8000 ENDPOINTS ===")
print("Models endpoint:")
print(subprocess.getoutput("curl -s http://127.0.0.1:8000/v1/models"))
print("\nHealth endpoint:")
print(subprocess.getoutput("curl -s http://127.0.0.1:8000/health"))
