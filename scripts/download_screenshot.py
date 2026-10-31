#!/usr/bin/env python3
import base64
import os
import subprocess

GIT_BASH = r"C:\Program Files\Git\bin\bash.exe"
EXECUTE_SCRIPT = r"C:/Users/farha/.gemini/config/skills/marimo-pair/scripts/execute-code.sh"
MOLAB_URL = "https://sb-91c0c5f9b81b2fa5.sb.molab.run/"
MOLAB_TOKEN = "b121e72f855e6aeb1abbeec604d2f150e59bf14b03588c651a287b8a7954166a"

cmd = [
    GIT_BASH,
    "-c",
    f'"{EXECUTE_SCRIPT}" --url {MOLAB_URL} --token {MOLAB_TOKEN} -'
]
res = subprocess.run(cmd, input='print(open("/marimo/chat_ui_screenshot.txt").read()[:50000])', text=True, capture_output=True)
print("Read snippet:", res.stdout[:100])
