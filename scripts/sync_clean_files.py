import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from safe_upload_files import upload_file_chunked

root = Path(__file__).resolve().parent.parent

print(">>> Uploading notebook.py...")
upload_file_chunked(root / "notebook.py", "/marimo/notebook.py")

print(">>> Uploading custom.css...")
upload_file_chunked(root / "custom.css", "/marimo/custom.css")

for folder in ["client", "runner", "tools", "config"]:
    src_folder = root / folder
    if src_folder.exists():
        for file_path in src_folder.iterdir():
            if file_path.is_file() and (file_path.suffix in [".py", ".yaml"]):
                dst_path = f"/marimo/model_package/{folder}/{file_path.name}"
                print(f">>> Uploading {file_path.name} -> {dst_path}...")
                upload_file_chunked(file_path, dst_path)

print(">>> All clean files uploaded successfully!")
