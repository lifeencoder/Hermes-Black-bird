#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hermes Black Bird - AgentRunner & Tool Loop Verification Script
Tests multi-step tool execution with Hermes-3-Llama-3.1-70B-FP8 on vLLM.
Independent execution - zero external UI dependencies.
"""

import os
import sys
from pathlib import Path

# Ensure package root is in sys.path
package_root = Path(__file__).resolve().parent.parent
if str(package_root) not in sys.path:
    sys.path.insert(0, str(package_root))

from client.model_client import ModelClient
from runner.agent_runner import AgentRunner
from tools.builtin import register_builtin_tools
from tools.registry import ToolRegistry


def run_test():
    print("=" * 65)
    print("\U0001F985 Hermes Black Bird - AgentRunner & Tool Calling Verification")
    print("=" * 65)

    # 1. Initialize client
    print("[*] Initializing ModelClient...")
    client = ModelClient()
    if not client.check_connection():
        print(f"[!] ERROR: Cannot connect to vLLM server at {client.base_url}")
        sys.exit(1)
    print(f"[+] Connected to: {client.base_url} (Model: {client.model_name})")

    # 2. Initialize ToolRegistry with builtin tools
    print("[*] Registering builtin tools (get_current_time, calculate)...")
    registry = register_builtin_tools()
    registered_names = registry.list_tool_names()
    print(f"[+] Available tools: {registered_names}")
    print("-" * 65)

    # 3. Initialize AgentRunner
    runner = AgentRunner(model_client=client, tool_registry=registry, max_iterations=5)

    # 4. Prompt requiring both tools:
    # "الان ساعت چنده؟ و ۲۵ ضربدر ۴ چند میشه؟"
    user_prompt = "\u0627\u0644\u0627\u0646 \u0633\u0627\u0639\u062a \u0686\u0646\u062f\u0647\u061f \u0648 \u06f2\u06f5 \u0636\u0631\u0628\u062f\u0631 \u06f4 \u0686\u0646\u062f \u0645\u06cc\u0634\u0647\u061f"
    messages = [
        {"role": "user", "content": user_prompt}
    ]

    print(f"[*] User Prompt: \"{user_prompt}\"")
    print("[*] Starting AgentRunner loop...")
    print("-" * 65)

    result = runner.run(messages=messages, verbose=True)

    print("-" * 65)
    print(f"[+] Loop completed in {result['iterations']} iteration(s).")
    print(f"[+] Total tools executed: {len(result['executed_tools'])}")
    for idx, t in enumerate(result['executed_tools'], 1):
        print(f"    {idx}. Tool: '{t['name']}' | Args: {t['arguments']} => Result: {t['result']}")

    print("~" * 65)
    print("[*] Final Model Answer:")
    print(result["content"])
    print("~" * 65)

    if result["status"] == "success" and len(result["executed_tools"]) > 0:
        print("=" * 65)
        print("\u2705 ALL TESTS PASSED! AgentRunner and ToolRegistry are working perfectly.")
        print("=" * 65)
        return True
    else:
        print("[!] Warning: Loop completed but no tools were executed or unexpected status.")
        return False


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
