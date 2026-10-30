#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hermes Black Bird - MCP Integration Test Script
Validates full end-to-end tool calling via Model Context Protocol (MCP) with Hermes-3 70B on vLLM.
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
from tools.mcp_client import MCPClient
from tools.registry import ToolRegistry


def run_test():
    print("=" * 65)
    print("\U0001F985 Hermes Black Bird - MCP (Model Context Protocol) Verification")
    print("=" * 65)

    # 1. Locate dummy MCP server script
    server_script = Path(__file__).resolve().parent / "dummy_mcp_server.py"
    if not server_script.exists():
        print(f"[!] ERROR: Dummy server not found at {server_script}")
        sys.exit(1)

    print(f"[*] Target MCP Server: {server_script}")
    print(f"[*] Python Interpreter: {sys.executable}")

    # 2. Launch MCPClient over stdio
    print("[*] Spawning MCP stdio connection to server...")
    mcp_client = MCPClient(
        command=sys.executable,
        args=[str(server_script)],
    )

    try:
        mcp_client.start()
        print("[+] MCP Client connected successfully to server!")

        # 3. Discover and register MCP tools into ToolRegistry
        registry = ToolRegistry()
        registered = registry.register_mcp_tools(mcp_client)
        print(f"[+] Discovered & Registered MCP Tools: {registered}")
        print("-" * 65)

        # 4. Initialize ModelClient and AgentRunner
        print("[*] Initializing ModelClient and AgentRunner...")
        model_client = ModelClient()
        if not model_client.check_connection():
            print(f"[!] ERROR: Cannot reach vLLM server at {model_client.base_url}")
            sys.exit(1)

        runner = AgentRunner(model_client=model_client, tool_registry=registry, max_iterations=5)

        # 5. Prompt requiring system info tool
        # "مشخصات سیستم را بررسی کن و گزارش بده"
        user_prompt = "\u0645\u0634\u062e\u0635\u0627\u062a \u0633\u06cc\u0633\u062a\u0645 \u0631\u0627 \u0628\u0631\u0631\u0633\u06cc \u06a9\u0646 \u0648 \u06af\u0632\u0627\u0631\u0634 \u0628\u062f\u0647"
        messages = [
            {"role": "user", "content": user_prompt}
        ]

        print(f"[*] User Prompt: \"{user_prompt}\"")
        print("[*] Executing AgentRunner with MCP-injected tools...")
        print("-" * 65)

        result = runner.run(messages=messages, verbose=True)

        print("-" * 65)
        print(f"[+] Loop completed in {result['iterations']} iteration(s).")
        print(f"[+] Tools executed through MCP protocol: {len(result['executed_tools'])}")
        for idx, t in enumerate(result['executed_tools'], 1):
            print(f"    {idx}. MCP Tool: '{t['name']}' | Args: {t['arguments']}")
            print(f"       Raw Server Output:\n       {t['result']}")

        print("~" * 65)
        print("[*] Final Model Answer:")
        print(result["content"])
        print("~" * 65)

        if result["status"] == "success" and len(result["executed_tools"]) > 0:
            print("=" * 65)
            print("\u2705 ALL TESTS PASSED! MCP Client and ToolRegistry integration is working perfectly.")
            print("=" * 65)
            return True
        else:
            print("[!] Warning: Test did not execute any MCP tools or unexpected status.")
            return False

    finally:
        print("[*] Closing MCP stdio session...")
        mcp_client.close()
        print("[+] MCP session closed cleanly.")


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
