import subprocess

print("=== DF -H ===")
print(subprocess.getoutput("df -h"))

print("\n=== MOUNTS ===")
print(subprocess.getoutput("mount | grep -E 'marimo|drive|cache'"))

print("\n=== SEARCHING FOR HF_CACHE OR MODELS ===")
print(subprocess.getoutput("find / -maxdepth 3 -name '*hf_cache*' -o -name '*Hermes*' 2>/dev/null"))

print("\n=== GOOGLE DRIVE SEARCH ===")
print(subprocess.getoutput("find / -maxdepth 3 -iname '*drive*' 2>/dev/null"))
