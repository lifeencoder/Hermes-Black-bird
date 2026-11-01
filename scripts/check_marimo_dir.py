import os
import subprocess

print("Contents of /marimo:")
for item in sorted(os.listdir("/marimo")):
    p = os.path.join("/marimo", item)
    if os.path.isdir(p):
        print(f"  [DIR]  {item}/")
    else:
        sz = os.path.getsize(p)
        print(f"  [FILE] {item} ({sz:,} bytes)")

print("\nContents of /marimo/hf_cache:")
if os.path.exists("/marimo/hf_cache"):
    print(subprocess.getoutput("ls -la /marimo/hf_cache"))
else:
    print("/marimo/hf_cache does not exist")
