import subprocess

print("=== FIND HF_CACHE / HERMES ===")
print(subprocess.getoutput("find / -iname '*hf_cache*' 2>/dev/null"))
print(subprocess.getoutput("find / -iname '*hermes-3*' 2>/dev/null"))

print("\n=== HOME MARIMO ===")
print(subprocess.getoutput("ls -la /home/marimo"))

print("\n=== ROOT ===")
print(subprocess.getoutput("ls -la /root"))

print("\n=== MNT ===")
print(subprocess.getoutput("ls -la /mnt"))
