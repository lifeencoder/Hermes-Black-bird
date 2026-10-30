#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hermes Black Bird - Client Test Script
Validates ModelClient functionality and streaming responses from Hermes-3 vLLM endpoint.
Independent execution - does not require UI or browser.
"""

import os
import sys
from pathlib import Path

# Ensure the package root is in sys.path
package_root = Path(__file__).resolve().parent.parent
if str(package_root) not in sys.path:
    sys.path.insert(0, str(package_root))

from client.model_client import ModelClient


def run_test():
    print("=" * 60)
    print("\U0001F985 Hermes Black Bird - ModelClient Streaming Verification")
    print("=" * 60)

    # 1. Initialize client
    client = ModelClient()
    print("[*] Configuration Loaded:")
    print(f"    - Base URL:    {client.base_url}")
    print(f"    - Model Name:  {client.model_name}")
    print(f"    - Temperature: {client.default_temperature}")
    print(f"    - Max Tokens:  {client.default_max_tokens}")
    print("-" * 60)

    # 2. Check connectivity
    print("[*] Testing server connectivity...")
    if not client.check_connection():
        print(f"[!] ERROR: Cannot connect to vLLM server at {client.base_url}")
        print("    Please ensure the vLLM server is running.")
        sys.exit(1)

    available_models = client.list_models()
    print(f"[+] Server is ONLINE! Available models: {available_models}")
    print("-" * 60)

    # 3. Test streaming prompt with clean unicode escape
    # "\u0633\u0644\u0627\u0645\u060c \u062e\u0648\u062f\u062a \u0631\u0627 \u0645\u0639\u0631\u0641\u06cc \u06a9\u0646" = "سلام، خودت را معرفی کن"
    test_prompt = "\u0633\u0644\u0627\u0645\u060c \u062e\u0648\u062f\u062a \u0631\u0627 \u0645\u0639\u0631\u0641\u06cc \u06a9\u0646"
    messages = [
        {"role": "user", "content": test_prompt}
    ]

    print(f"[*] Sending prompt: \"{test_prompt}\"")
    print("[*] Streaming model response:")
    print("~" * 60)

    try:
        response_stream = client.chat(messages=messages, stream=True)
        full_content = ""
        for chunk in response_stream:
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    text_piece = delta.content
                    full_content += text_piece
                    sys.stdout.write(text_piece)
                    sys.stdout.flush()

        print("\n" + "~" * 60)
        print(f"[+] Streaming completed successfully ({len(full_content)} characters received).")
        print("=" * 60)
        print("\u2705 ALL TESTS PASSED! ModelClient is completely functional.")
        print("=" * 60)
        return True
    except Exception as err:
        print(f"\n[!] ERROR during chat streaming: {err}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_test()
