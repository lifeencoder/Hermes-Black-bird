import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from safe_upload_files import upload_file_chunked
from remote_exec import run_code

run_code("import os; os.makedirs('/marimo/model_package/config', exist_ok=True)")
root = Path(__file__).resolve().parent.parent
upload_file_chunked(root / "config" / "model.yaml", "/marimo/model_package/config/model.yaml")
