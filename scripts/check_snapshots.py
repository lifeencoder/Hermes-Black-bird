import subprocess

print("=== CHECKING SNAPSHOTS ===")
print(subprocess.getoutput("ls -lh /marimo/hf_cache/hub/models--NousResearch--Hermes-3-Llama-3.1-70B-FP8/snapshots/*/"))
