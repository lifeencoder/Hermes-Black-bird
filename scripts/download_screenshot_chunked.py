import os
import sys
import base64
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import subprocess

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
MOLAB_URL = os.getenv("MOLAB_URL", "https://sb-a792c711c6610d41.sb.molab.run/")
MOLAB_TOKEN = os.getenv("MOLAB_TOKEN", "")

def run_remote(code: str) -> str:
    cmd = [GIT_BASH, "-c", f'"{EXECUTE_SCRIPT}" --url {MOLAB_URL} --token {MOLAB_TOKEN} -']
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
    stdout, stderr = proc.communicate(input=code)
    return stdout

def download_file(remote_path: str, local_path: Path, chunk_size: int = 30000):
    size_out = run_remote(f"import os; print(os.path.getsize({repr(remote_path)}))")
    lines = [l.strip() for l in size_out.splitlines() if l.strip().isdigit()]
    if not lines:
        print("Failed to get file size:", size_out)
        return False
    total_size = int(lines[-1])
    print(f"Downloading {remote_path} ({total_size} bytes) -> {local_path}...")

    all_data = bytearray()
    for offset in range(0, total_size, chunk_size):
        length = min(chunk_size, total_size - offset)
        code = f"""import base64
with open({repr(remote_path)}, 'rb') as f:
    f.seek({offset})
    chunk = f.read({length})
print('CHUNK_B64:' + base64.b64encode(chunk).decode('ascii'))
"""
        res = run_remote(code)
        for line in res.splitlines():
            if line.startswith("CHUNK_B64:"):
                b64_str = line[len("CHUNK_B64:"):].strip()
                all_data.extend(base64.b64decode(b64_str))
                print(f"  Got chunk {offset}..{offset+length} ({len(all_data)}/{total_size})")
                break

    local_path.parent.mkdir(parents=True, exist_ok=True)
    with open(local_path, "wb") as f:
        f.write(all_data)
    print(f"Saved {len(all_data)} bytes to {local_path}")
    return True

if __name__ == "__main__":
    out_file = Path(r"C:\Users\farha\.gemini\antigravity\brain\b3bd5899-7441-41f4-9c91-cbdf156ca440\molab_ui_verified.png")
    download_file("/marimo/molab_ui_verified.png", out_file)
