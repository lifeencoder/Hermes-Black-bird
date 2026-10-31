import json
import subprocess

# Let's inspect hexstrike_server.py or how execute_command is handled
code = """
with open('/marimo/hexstrike-ai/hexstrike_server.py', 'r') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'def execute_command', text)]
for idx in matches:
    print(text[max(0, idx-50):min(len(text), idx+500)])
    print('='*50)
"""
print(code)
