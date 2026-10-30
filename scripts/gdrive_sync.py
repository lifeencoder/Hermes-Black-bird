#!/usr/bin/env python3
"""
Hermes Black Bird - Google Drive Model Sync & Backup Utility
Uses gdrive_fsspec to sync Hugging Face model cache with Google Drive.
"""

import os
import sys
import time
from gdrive_fsspec import GoogleDriveFileSystem

def sync_model_to_drive(
    local_cache: str = "/marimo/hf_cache",
    remote_base: str = "/hf_models/hermes-3-70b-fp8",
    token: str = "cache"
):
    print(f"Connecting to Google Drive with token='{token}'...")
    try:
        fs = GoogleDriveFileSystem(token=token)
        print("Connected successfully.")
    except Exception as e:
        print(f"Error connecting to Google Drive: {e}")
        return False

    # Check local model folder
    model_dir = None
    for root, dirs, files in os.walk(local_cache):
        if "config.json" in files and "Hermes-3" in root:
            model_dir = root
            break

    if not model_dir:
        print(f"Model directory not found in {local_cache}")
        return False

    print(f"Found model directory: {model_dir}")
    total_files = sum(len(files) for _, _, files in os.walk(model_dir))
    total_size = sum(
        os.path.getsize(os.path.join(root, f))
        for root, _, files in os.walk(model_dir) for f in files
    )
    print(f"Total files: {total_files}, Total size: {total_size / (1024**3):.2f} GB")

    try:
        fs.mkdirs(remote_base, exist_ok=True)
    except Exception:
        pass

    start_time = time.time()
    copied = 0
    skipped = 0

    for root, _, files in os.walk(model_dir):
        for f in files:
            src = os.path.join(root, f)
            rel = os.path.relpath(src, model_dir).replace("\\", "/")
            dst = f"{remote_base}/{rel}"
            size = os.path.getsize(src)

            # Resume-friendly: check if already exists
            try:
                if fs.exists(dst):
                    info = fs.info(dst)
                    if info.get("size") == size:
                        skipped += 1
                        continue
            except Exception:
                pass

            # Ensure remote directory exists
            try:
                fs.mkdirs(os.path.dirname(dst), exist_ok=True)
            except Exception:
                pass

            with open(src, "rb") as fsrc, fs.open(dst, "wb") as fdst:
                fdst.write(fsrc.read())

            copied += 1
            elapsed = time.time() - start_time
            print(f"[{copied + skipped}/{total_files}] Copied: {rel} ({elapsed:.1f}s)")

    duration = time.time() - start_time
    print("==================================================")
    print(f"Sync complete! Copied: {copied}, Skipped: {skipped}")
    print(f"Duration: {duration:.1f}s")
    print("==================================================")
    return True

if __name__ == "__main__":
    sync_model_to_drive()
