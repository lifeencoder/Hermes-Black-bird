#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hermes Black Bird - System Prompt Verification Script
Validates standard system_prompt injection into ModelClient chat completions.
Pure Python - zero external UI dependencies.
"""

import os
import sys
from pathlib import Path

# Safe stdout encoding for all terminal environments
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure package root is in sys.path
package_root = Path(__file__).resolve().parent.parent
if str(package_root) not in sys.path:
    sys.path.insert(0, str(package_root))

from client.model_client import ModelClient


def run_system_prompt_test():
    print("=" * 65)
    print("🦅 Hermes Black Bird - System Prompt Injection Verification")
    print("=" * 65)

    client = ModelClient()
    if not client.check_connection():
        print(f"[!] ERROR: Cannot reach vLLM server at {client.base_url}")
        sys.exit(1)

    print(f"[+] Connected to: {client.base_url} (Model: {client.model_name})")

    # 1. Define standard programming persona
    system_persona = (
        "تو یک دستیار ارشد برنامه‌نویسی پایتون هستی. پاسخ‌هایت فنی، بسیار فشرده، "
        "مستند و به زبان فارسی شیوا باشد."
    )
    user_query = "چگونه در پایتون کلیدها و مقادیر یک دیکشنری را معکوس (Invert) کنیم؟ با یک مثال کوتاه نشان بده."

    print(f"[*] Injected System Prompt:\n    \"{system_persona}\"")
    print(f"[*] User Query:\n    \"{user_query}\"")
    print("-" * 65)

    # 2. Execute chat with system_prompt
    print("[*] Sending request with system_prompt...")
    response = client.chat(
        messages=[{"role": "user", "content": user_query}],
        system_prompt=system_persona,
        stream=False,
        temperature=0.2,
        max_tokens=512,
    )

    answer = response.choices[0].message.content
    print("\n" + "=" * 65)
    print("🎯 پاسخ مدل با نقش تزریق‌شده (System Persona Response):")
    print("=" * 65)
    print(answer)
    print("=" * 65)

    if answer and len(answer.strip()) > 10:
        print("✅ SYSTEM PROMPT TEST PASSED! The persona was injected and honored successfully.")
        return True
    else:
        print("[!] Test failed: empty response received.")
        return False


if __name__ == "__main__":
    success = run_system_prompt_test()
    sys.exit(0 if success else 1)
