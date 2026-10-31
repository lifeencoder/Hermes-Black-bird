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

GIT_BASH = r"C:\Program Files\Git\bin\bash.exe"
EXECUTE_SCRIPT = r"C:/Users/farha/.gemini/config/skills/marimo-pair/scripts/execute-code.sh"
MOLAB_URL = os.getenv("MOLAB_URL", "https://sb-91c0c5f9b81b2fa5.sb.molab.run/")
MOLAB_TOKEN = os.getenv("MOLAB_TOKEN", "")

code = """
import base64
with open('/marimo/notebook.py', 'rb') as f:
    data = f.read()
print('===B64_START===')
print(base64.b64encode(data).decode('ascii'))
print('===B64_END===')
"""

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
stdout, stderr = proc.communicate(input=code)

if "===B64_START===" in stdout and "===B64_END===" in stdout:
    b64_str = stdout.split("===B64_START===")[1].split("===B64_END===")[0].strip()
    content = base64.b64decode(b64_str)
    with open("notebook.py", "wb") as f:
        f.write(content)
    print(f"[OK] Downloaded /marimo/notebook.py ({len(content)} bytes) to local notebook.py")
else:
    print("Error pulling notebook.py:")
    print(stdout)
    print(stderr)
