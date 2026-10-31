import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from download_screenshot_chunked import download_file

root = Path(r"C:\Users\farha\.gemini\antigravity\brain\b3bd5899-7441-41f4-9c91-cbdf156ca440")
local_dest = root / "molab_ui_streamlined.png"

download_file("/marimo/molab_ui_streamlined.png", local_dest)
print("Saved to", local_dest)
