with open('/marimo/notebook.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("File length:", len(text))
# Check _mcp_path or _mcp_candidates
for line in text.splitlines():
    if '_mcp' in line or 'endpoint_url' in line or '8000' in line or '8888' in line:
        print(line)
