import subprocess

print("=== CHECKING HF_CACHE SIZE ===")
print(subprocess.getoutput("du -sh /marimo/hf_cache/* 2>/dev/null || echo 'empty'"))
print("\n=== TOTAL /marimo/hf_cache SIZE ===")
print(subprocess.getoutput("du -sh /marimo/hf_cache"))
