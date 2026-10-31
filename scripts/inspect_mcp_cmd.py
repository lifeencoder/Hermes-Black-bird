with open('/marimo/hexstrike-ai/hexstrike_mcp.py', 'r') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'execute_command', text)]
for idx in matches:
    print(text[max(0, idx-100):min(len(text), idx+300)])
    print('='*50)
