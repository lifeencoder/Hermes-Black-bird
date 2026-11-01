import hashlib
import os

with open("/marimo/custom.css", "rb") as f:
    h = hashlib.sha256(f.read()).hexdigest()
print("Remote /marimo/custom.css SHA256:", h)
print("Size:", os.path.getsize("/marimo/custom.css"))
