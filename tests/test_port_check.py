#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script verifying ModelClient with default engineering system prompt
and optimized inference parameters (temperature=0.8, top_p=0.95, presence_penalty=0.1).
Requests a clean Python socket-based server port availability check script.
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

# Ensure model_package / root is in path
package_root = Path(__file__).resolve().parent.parent
if str(package_root) not in sys.path:
    sys.path.insert(0, str(package_root))

# Also check MoLab path
if os.path.exists("/marimo/model_package") and "/marimo/model_package" not in sys.path:
    sys.path.insert(0, "/marimo/model_package")

from client.model_client import ModelClient


def run_test():
    print("=" * 65)
    print("🦅 Hermes Black Bird - Port Availability Check Code Generation Test")
    print("=" * 65)

    client = ModelClient()
    print(f"[*] Base URL:           {client.base_url}")
    print(f"[*] Model Name:         {client.model_name}")
    print(f"[*] Temperature:        {client.default_temperature}")
    print(f"[*] Top P:              {client.default_top_p}")
    print(f"[*] Presence Penalty:   {client.default_presence_penalty}")
    print(f"[*] Default Sys Prompt: {client.default_system_prompt[:65]}...")
    print("-" * 65)

    # Prompt: بررسی باز بودن پورت‌های یک سرور با استفاده از سوکت
    prompt = (
        "لطفاً یک اسکریپت تمیز، بهینه و ساختاریافته به زبان پایتون بنویس که "
        "با استفاده از کتابخانه استاندارد socket، باز بودن یا در دسترس بودن پورت‌های یک سرور "
        "(مانند پورت‌های 80، 443، 8000 و 22) را بررسی کند. کد باید شامل مدیریت خطا و تایم‌اوت باشد."
    )

    print(f"[*] Sending user prompt:\n    \"{prompt}\"\n")
    print("[*] Waiting for model completion...")

    response = client.chat(
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )

    reply = response.choices[0].message.content

    print("=" * 65)
    print("📝 خروجی دریافتی از مدل:")
    print("=" * 65)
    print(reply)
    print("=" * 65)
    print("✅ TEST COMPLETED SUCCESSFULLY!")


if __name__ == "__main__":
    run_test()
