#!/usr/bin/env python3
"""
Sync local model package files to MoLab container at /marimo/model_package/
Uses Base64 encoding to guarantee 100% safe transmission across Windows shells.
"""

import os
import sys
import base64
import subprocess
from pathlib import Path

def _load_env():
    env_file = Path(__file__).resolve().parent.parent / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    if k.strip() not in os.environ:
                        os.environ[k.strip()] = v.strip().strip("'\"")

_load_env()

LOCAL_ROOT = Path(__file__).resolve().parent.parent
DIRS_TO_SYNC = ["config", "client", "runner", "tools", "tests"]
MOLAB_URL = os.getenv("MOLAB_URL", "https://sb-91c0c5f9b81b2fa5.sb.molab.run/")
MOLAB_TOKEN = os.getenv("MOLAB_TOKEN", "")
GIT_BASH = r"C:\Program Files\Git\bin\bash.exe"
EXECUTE_SCRIPT = r"C:/Users/farha/.gemini/config/skills/marimo-pair/scripts/execute-code.sh"


def run_code_in_molab(python_code: str) -> bool:
    cmd = [
        GIT_BASH,
        "-c",
        f'"{EXECUTE_SCRIPT}" --url {MOLAB_URL} --token {MOLAB_TOKEN} -'
    ]
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8"
    )
    stdout, stderr = proc.communicate(input=python_code)
    if proc.returncode != 0:
        print(f"Error ({proc.returncode}): {stderr or stdout}")
        return False
    return True


def sync_file(rel_path: str, content_bytes: bytes) -> bool:
    chunk_size = 12000
    if len(content_bytes) <= chunk_size:
        b64_str = base64.b64encode(content_bytes).decode("ascii")
        remote_code = f"""
import os, base64
target = os.path.join('/marimo/model_package', {repr(rel_path)})
os.makedirs(os.path.dirname(target), exist_ok=True)
data = base64.b64decode('{b64_str}')
with open(target, 'wb') as f:
    f.write(data)
print(f'Synced: {{target}} ({{len(data)}} bytes)')
"""
        return run_code_in_molab(remote_code)
    else:
        # Chunked upload for large files
        remote_init = f"""
import os
target = os.path.join('/marimo/model_package', {repr(rel_path)})
os.makedirs(os.path.dirname(target), exist_ok=True)
with open(target, 'wb') as f:
    pass
"""
        if not run_code_in_molab(remote_init):
            return False
        for i in range(0, len(content_bytes), chunk_size):
            chunk = content_bytes[i:i + chunk_size]
            b64_chunk = base64.b64encode(chunk).decode("ascii")
            remote_append = f"""
import base64
target = os.path.join('/marimo/model_package', {repr(rel_path)})
with open(target, 'ab') as f:
    f.write(base64.b64decode('{b64_chunk}'))
"""
            if not run_code_in_molab(remote_append):
                return False
        return True


def sync():
    files_to_sync = []
    for dir_name in DIRS_TO_SYNC:
        dir_path = LOCAL_ROOT / dir_name
        if not dir_path.exists():
            continue
        for file_path in dir_path.rglob("*"):
            if file_path.is_file() and not file_path.name.endswith(".pyc"):
                rel_path = file_path.relative_to(LOCAL_ROOT).as_posix()
                files_to_sync.append((rel_path, file_path))

    print(f"[*] Synchronizing {len(files_to_sync)} files to MoLab (/marimo/model_package)...")
    success_count = 0
    for rel_path, file_path in files_to_sync:
        with open(file_path, "rb") as f:
            content_bytes = f.read()
        print(f"  -> Uploading: {rel_path} ({len(content_bytes)} bytes)...", end=" ", flush=True)
        if sync_file(rel_path, content_bytes):
            print("OK")
            success_count += 1
        else:
            print("FAILED")

    print(f"\n[*] Result: {success_count}/{len(files_to_sync)} files synchronized successfully.")

    # Verify listing in MoLab
    verify_code = """
import os
target_base = '/marimo/model_package'
print('[MoLab] Current files in /marimo/model_package:')
for root, dirs, fnames in os.walk(target_base):
    if '__pycache__' in root:
        continue
    for fn in fnames:
        p = os.path.relpath(os.path.join(root, fn), target_base)
        print('  -', p)
"""
    cmd = [
        GIT_BASH,
        "-c",
        f'"{EXECUTE_SCRIPT}" --url {MOLAB_URL} --token {MOLAB_TOKEN} -'
    ]
    proc = subprocess.run(cmd, input=verify_code, text=True, capture_output=True, encoding="utf-8")
    print(proc.stdout)
    return success_count == len(files_to_sync)


if __name__ == "__main__":
    ok = sync()
    sys.exit(0 if ok else 1)
