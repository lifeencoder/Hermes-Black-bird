import os
import sys
import base64
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from remote_exec import run_code

def upload_file_chunked(local_path: Path, remote_path: str, chunk_size: int = 10000):
    print(f"Uploading {local_path.name} -> {remote_path}...")
    with open(local_path, "rb") as f:
        data = f.read()

    # Clear remote file
    run_code(f"with open({repr(remote_path)}, 'wb') as f: pass")

    total_chunks = (len(data) + chunk_size - 1) // chunk_size
    for idx, i in enumerate(range(0, len(data), chunk_size), 1):
        chunk = data[i:i + chunk_size]
        b64 = base64.b64encode(chunk).decode("ascii")
        code = f"""import base64
with open({repr(remote_path)}, 'ab') as f:
    f.write(base64.b64decode('{b64}'))
"""
        run_code(code)
        print(f"  [{idx}/{total_chunks}] chunk uploaded ({len(chunk)} bytes)")

    # Verify
    verify_code = f"""import os
print(f'Verified: {{os.path.basename({repr(remote_path)})}} is {{os.path.getsize({repr(remote_path)})}} bytes on MoLab')
"""
    run_code(verify_code)

if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    upload_file_chunked(root / "notebook.py", "/marimo/notebook.py")
    upload_file_chunked(root / "custom.css", "/marimo/custom.css")
