import hashlib
import os

print("=== CHECKING MOLAB NOTEBOOK HASH ===")
if os.path.exists("/marimo/notebook.py"):
    with open("/marimo/notebook.py", "rb") as f:
        h = hashlib.sha256(f.read()).hexdigest()
    print("Remote /marimo/notebook.py SHA256:", h)
    print("Size:", os.path.getsize("/marimo/notebook.py"))
