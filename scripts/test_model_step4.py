#!/usr/bin/env python3
"""
Step 4: ModelClient verification test for Hermes-3.
"""
import sys
import os

# Ensure model_package is in path
sys.path.insert(0, "/marimo/model_package")

from client.model_client import ModelClient

print("=== STEP 4: ModelClient Verification Test ===")
config_path = "/marimo/model_package/config/model.yaml"
client = ModelClient(config_path=config_path)

# "یک جمله درباره قانون جاذبه نیوتن بگو"
prompt = "\u06cc\u06a9 \u062c\u0645\u0644\u0647 \u062f\u0631\u0628\u0627\u0631\u0647 \u0642\u0627\u0646\u0648\u0646 \u062c\u0627\u0630\u0628\u0647 \u0646\u06cc\u0648\u062a\u0646 \u0628\u06af\u0648"
messages = [{"role": "user", "content": prompt}]

print(f"Prompt sent: {prompt}\n")
response = client.chat(messages=messages, stream=False)

reply = response.choices[0].message.content
print("=== Model Response ===")
print(reply)
print("\n[✓] Step 4 completed successfully!")
