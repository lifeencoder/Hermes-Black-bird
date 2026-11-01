import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from safe_upload_files import upload_file_chunked
from remote_exec import run_code

root = Path(__file__).resolve().parent.parent
upload_file_chunked(root / "scripts" / "run_eval_script.py", "/marimo/run_eval_script.py")

launch_code = """
import subprocess
import os

p = subprocess.Popen(
    ['/tmp/uv-venv/bin/python', '-u', '/marimo/run_eval_script.py'],
    start_new_session=True,
    stdout=open('/marimo/persian_test_output.txt', 'w'),
    stderr=subprocess.STDOUT,
    stdin=subprocess.DEVNULL
)
print(f'Started evaluation detached with PID: {p.pid}')
"""
run_code(launch_code)
