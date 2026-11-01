import subprocess

print("=== CHECKING FOR MODEL WEIGHTS ===")
print("find hub in /home and /root and /marimo:")
print(subprocess.getoutput("find /home /root /marimo -type d -name '*Hermes*' 2>/dev/null"))
print("\nfind huggingface hub:")
print(subprocess.getoutput("find /home /root /marimo /tmp -name '*hub*' 2>/dev/null | head -n 30"))
print("\ncheck disk space on all mounts:")
print(subprocess.getoutput("df -h"))
