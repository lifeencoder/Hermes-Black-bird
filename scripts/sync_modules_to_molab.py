import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from safe_upload_files import upload_file_chunked

def sync_all_modules():
    root = Path(__file__).resolve().parent.parent
    for folder in ["client", "runner", "tools", "config"]:
        src_dir = root / folder
        if src_dir.exists():
            for f in src_dir.glob("*.py"):
                upload_file_chunked(f, f"/marimo/model_package/{folder}/{f.name}")
            for f in src_dir.glob("*.yaml"):
                upload_file_chunked(f, f"/marimo/model_package/{folder}/{f.name}")
    print("Module packages synced!")

if __name__ == "__main__":
    sync_all_modules()
