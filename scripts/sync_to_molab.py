#!/usr/bin/env python3
"""
Sync local model package files to MoLab container at /marimo/model_package/
"""

import os
import sys
import json
import subprocess
from pathlib import Path

LOCAL_ROOT = Path(__file__).resolve().parent.parent
DIRS_TO_SYNC = ["config", "client", "runner", "tools", "tests"]
MOLAB_URL = "https://sb-d1dcf65203f25955.sb.molab.run/"
MOLAB_TOKEN = "982d2a7c2f450b665e578781ab35321f2b74653c495e9107f3476101d7130570"
GIT_BASH = r"C:\Program Files\Git\bin\bash.exe"
EXECUTE_SCRIPT = r"C:/Users/farha/.gemini/config/skills/marimo-pair/scripts/execute-code.sh"

def build_payload():
    files_data = {}
    for dir_name in DIRS_TO_SYNC:
        dir_path = LOCAL_ROOT / dir_name
        if not dir_path.exists():
            continue
        for file_path in dir_path.rglob("*"):
            if file_path.is_file():
                rel_path = file_path.relative_to(LOCAL_ROOT).as_posix()
                with open(file_path, "r", encoding="utf-8") as f:
                    files_data[rel_path] = f.read()
    return files_data

def sync():
    files = build_payload()
    print(f"[*] Packaging {len(files)} files for synchronization:")
    for p in files.keys():
        print(f"    - {p}")

    remote_python_code = f"""
import os, sys

files = {json.dumps(files, ensure_ascii=False)}
target_base = "/marimo/model_package"

print(f"[*] Synchronizing {{len(files)}} files into {{target_base}}...")
for rel_path, content in files.items():
    full_path = os.path.join(target_base, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"    [+] Written: {{rel_path}} ({{len(content)}} chars)")

print("[+] Synchronizing complete. Listing /marimo/model_package:")
for root, dirs, fnames in os.walk(target_base):
    for fn in fnames:
        p = os.path.relpath(os.path.join(root, fn), target_base)
        print("    -", p)
"""

    print("\n[*] Sending payload to MoLab via marimo-pair bridge...")
    cmd = [
        GIT_BASH,
        "-c",
        f'"{EXECUTE_SCRIPT}" --url {MOLAB_URL} --token {MOLAB_TOKEN} -'
    ]

    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8"
    )

    out, _ = proc.communicate(input=remote_python_code)
    print("\n--- MoLab Remote Response ---")
    print(out)
    return proc.returncode == 0

if __name__ == "__main__":
    success = sync()
    sys.exit(0 if success else 1)
