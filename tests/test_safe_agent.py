#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hermes Black Bird - Safe Agent Integration Test
Demonstrates end-to-end autonomous agent workflow connecting to a standard MCP server
(mock_custom_mcp.py) and executing verified benign tools via AgentRunner.
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
from runner.agent_runner import AgentRunner
from tools.mcp_client import MCPClient
from tools.registry import ToolRegistry


def run_safe_agent_test():
    print("=" * 65)
    print("🦅 Hermes Black Bird - Safe MCP Agent Execution Test")
    print("=" * 65)

    # 1. Locate mock MCP server
    server_path = Path(__file__).resolve().parent / "mock_custom_mcp.py"
    if not server_path.exists():
        print(f"[!] ERROR: Mock server not found at: {server_path}")
        sys.exit(1)

    print(f"[*] Target MCP Server:    {server_path}")
    print(f"[*] Python Interpreter:   {sys.executable}")

    # 2. Start MCPClient over stdio
    print("\n[*] Initializing MCPClient over stdio...")
    mcp_client = MCPClient(
        command=sys.executable,
        args=[str(server_path)],
        startup_timeout=20.0,
    )

    try:
        mcp_client.start()
        print("[+] MCP Client connected to server process!")

        # 3. Discover and register tools into ToolRegistry
        registry = ToolRegistry()
        registered_tools = registry.register_mcp_tools(mcp_client)
        print(f"[+] Discovered & Registered {len(registered_tools)} MCP tools into ToolRegistry.")
        print(f"    Available: {registered_tools}")
        print("-" * 65)

        # 4. Initialize ModelClient and AgentRunner
        print("[*] Initializing ModelClient and AgentRunner...")
        model = ModelClient()
        if not model.check_connection():
            print(f"[!] Warning: vLLM server offline at {model.base_url}. Skipping live model call.")
            return True

        runner = AgentRunner(model_client=model, tool_registry=registry, max_iterations=5)

        # 5. Safe Prompt for invoking echo_message tool
        prompt = (
            "لطفاً با استفاده از ابزار echo_message، پیام 'Hello from Hermes Black Bird' "
            "را به سرور بفرست و برچسب زمانی پاسخ سرور را گزارش بده."
        )
        messages = [{"role": "user", "content": prompt}]

        print(f"[*] User Prompt: \"{prompt}\"")
        print("[*] Executing AgentRunner loop...")
        print("-" * 65)

        result = runner.run(messages=messages, verbose=True)

        print("-" * 65)
        print(f"[+] Loop completed in {result['iterations']} iteration(s).")
        print(f"[+] Tools executed through MCP: {len(result['executed_tools'])}")
        for idx, t in enumerate(result['executed_tools'], 1):
            print(f"    {idx}. MCP Tool: '{t['name']}' | Args: {t['arguments']}")
            print(f"       Result: {t['result']}")

        print("~" * 65)
        print("[*] Final Model Answer:")
        print(result["content"])
        print("~" * 65)

        if result["status"] == "success" and len(result["executed_tools"]) > 0:
            print("=" * 65)
            print("✅ SAFE AGENT TEST PASSED! MCP Client and AgentRunner operate with full integrity.")
            print("=" * 65)
            return True
        else:
            print("[!] Note: Completed without tool execution or non-success status.")
            return False

    finally:
        print("[*] Shutting down MCPClient session...")
        mcp_client.close()
        print("[+] Session closed cleanly.")


if __name__ == "__main__":
    success = run_safe_agent_test()
    sys.exit(0 if success else 1)
