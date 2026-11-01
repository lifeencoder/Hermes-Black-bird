import os
import sys
import subprocess
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from safe_upload_files import upload_file_chunked
from remote_exec import run_code

root = Path(__file__).resolve().parent.parent

print("=== 1. SYNCING START.SH TO MOLAB ===")
upload_file_chunked(root / "start.sh", "/marimo/start.sh")

print("\n=== 2. EXECUTING /marimo/start.sh ON MOLAB ===")
exec_code = """
import subprocess
import os

os.chmod('/marimo/start.sh', 0o755)
out = subprocess.getoutput('bash /marimo/start.sh')
print(out)
"""
run_code(exec_code)
