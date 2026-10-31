#!/usr/bin/env python3
"""
Upload custom.css to MoLab in safe chunks.
"""
import base64
import os
import subprocess
import sys

MOLAB_URL = os.getenv("MOLAB_URL", "https://sb-91c0c5f9b81b2fa5.sb.molab.run/")
MOLAB_TOKEN = os.getenv("MOLAB_TOKEN", "b121e72f855e6aeb1abbeec604d2f150e59bf14b03588c651a287b8a7954166a")
GIT_BASH = r"C:\Program Files\Git\bin\bash.exe"
EXECUTE_SCRIPT = r"C:/Users/farha/.gemini/config/skills/marimo-pair/scripts/execute-code.sh"


def run_code(python_code: str):
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


def upload_css():
    css_path = "custom.css"
    if not os.path.exists(css_path):
        print("custom.css not found locally!")
        return False

    with open(css_path, "rb") as f:
        data = f.read()

    print(f"Uploading custom.css ({len(data)} bytes)...")
    run_code("open('/marimo/custom.css', 'wb').close()")

    chunk_size = 20000
    total_chunks = (len(data) + chunk_size - 1) // chunk_size

    for idx, i in enumerate(range(0, len(data), chunk_size), 1):
        chunk = data[i:i + chunk_size]
        b64 = base64.b64encode(chunk).decode("ascii")
        code = f"""import base64
with open('/marimo/custom.css', 'ab') as f:
    f.write(base64.b64decode('{b64}'))
"""
        ok = run_code(code)
        if not ok:
            print(f"Failed on chunk {idx}/{total_chunks}")
            return False
        print(f"Chunk {idx}/{total_chunks} uploaded.")

    # Verify
    verify_code = """import os
print('Uploaded /marimo/custom.css size:', os.path.getsize('/marimo/custom.css'))
"""
    cmd = [
        GIT_BASH,
        "-c",
        f'"{EXECUTE_SCRIPT}" --url {MOLAB_URL} --token {MOLAB_TOKEN} -'
    ]
    res = subprocess.run(cmd, input=verify_code, text=True, capture_output=True, encoding="utf-8")
    print(res.stdout)
    return True


if __name__ == "__main__":
    upload_css()
