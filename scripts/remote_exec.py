#!/usr/bin/env python3
"""
Remote execution helper for MoLab container.
"""

import os
import sys
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


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

MOLAB_URL = os.getenv("MOLAB_URL", "https://sb-91c0c5f9b81b2fa5.sb.molab.run/")
MOLAB_TOKEN = os.getenv("MOLAB_TOKEN", "")
GIT_BASH = r"C:\Program Files\Git\bin\bash.exe"
EXECUTE_SCRIPT = r"C:/Users/farha/.gemini/config/skills/marimo-pair/scripts/execute-code.sh"


def run_code(python_code: str):
    if not MOLAB_TOKEN:
        print("Error: MOLAB_TOKEN environment variable not set. Please configure .env file.", file=sys.stderr)
        sys.exit(1)

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
    if stdout:
        print(stdout, end="")
    if stderr:
        print(stderr, file=sys.stderr, end="")
    sys.exit(proc.returncode)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "-c" and len(sys.argv) > 2:
            code = sys.argv[2]
        else:
            with open(sys.argv[1], "r", encoding="utf-8") as f:
                code = f.read()
    else:
        code = sys.stdin.read()
    run_code(code)
