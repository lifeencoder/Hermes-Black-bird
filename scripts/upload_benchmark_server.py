import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync_to_molab import sync_file

local_file = Path(__file__).resolve().parent.parent / "tests" / "benchmark_150_tools_server.py"
print(f"Uploading {local_file.name} ({local_file.stat().st_size} bytes)...")
with open(local_file, "rb") as f:
    success = sync_file("tests/benchmark_150_tools_server.py", f.read())

if success:
    print("[OK] Uploaded benchmark_150_tools_server.py successfully.")
else:
    print("[FAIL] Failed to upload benchmark_150_tools_server.py.")
    sys.exit(1)
