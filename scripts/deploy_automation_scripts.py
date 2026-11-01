import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from safe_upload_files import upload_file_chunked
from remote_exec import run_code

def deploy_and_start():
    root = Path(__file__).resolve().parent.parent

    print("=== STEP 1: UPLOADING AUTOMATION SCRIPTS ===")
    upload_file_chunked(root / "start.sh", "/marimo/start.sh")
    upload_file_chunked(root / "bootstrap.sh", "/marimo/bootstrap.sh")
    upload_file_chunked(root / "custom.css", "/marimo/custom.css")
    upload_file_chunked(root / "notebook.py", "/marimo/notebook.py")

    print("\n=== STEP 2: CHMOD +X AND RUN START.SH DETACHED ===")
    launch_code = """
import os
import subprocess

os.chmod('/marimo/start.sh', 0o755)
os.chmod('/marimo/bootstrap.sh', 0o755)

p = subprocess.Popen(
    ['/bin/bash', '/marimo/start.sh'],
    start_new_session=True,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    stdin=subprocess.DEVNULL
)
print(f'Started /marimo/start.sh detached with PID: {p.pid}')
"""
    run_code(launch_code)

if __name__ == "__main__":
    deploy_and_start()
