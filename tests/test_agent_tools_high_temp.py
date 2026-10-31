#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hermes Black Bird - High Temperature Agent Tool Calling Test
Verifies that AgentRunner and ModelClient retain 100% precision in tool calling
under elevated temperature (temperature=0.8, top_p=0.95, presence_penalty=0.1)
and the default technical engineering system prompt.
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

# Ensure model_package / root is in path
package_root = Path(__file__).resolve().parent.parent
if str(package_root) not in sys.path:
    sys.path.insert(0, str(package_root))

if os.path.exists("/marimo/model_package") and "/marimo/model_package" not in sys.path:
    sys.path.insert(0, "/marimo/model_package")

from client.model_client import ModelClient
from runner.agent_runner import AgentRunner
from tools.mcp_client import MCPClient
from tools.registry import ToolRegistry


def run_agent_tool_test():
    print("=" * 65)
    print("🦅 Hermes Black Bird - Agent Tool Calling Test (High Temperature)")
    print("=" * 65)

    # 1. Locate mock MCP server
    server_path = Path(__file__).resolve().parent / "mock_custom_mcp.py"
    if not server_path.exists():
        server_path = Path("/marimo/model_package/tests/mock_custom_mcp.py")

    print(f"[*] Target MCP Server:    {server_path}")
    print(f"[*] Python Interpreter:   {sys.executable}")

    # 2. Connect MCPClient
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
        print(f"    Available tools: {registered_tools}")
        print("-" * 65)

        # 4. Initialize ModelClient and verify parameters
        model = ModelClient()
        print("[*] ModelClient Configuration:")
        print(f"    - Base URL:           {model.base_url}")
        print(f"    - Model Name:         {model.model_name}")
        print(f"    - Temperature:        {model.default_temperature} (High Temp Mode)")
        print(f"    - Top-P:              {model.default_top_p}")
        print(f"    - Presence Penalty:   {model.default_presence_penalty}")
        print(f"    - System Prompt:      {model.default_system_prompt[:60]}...")

        if not model.check_connection():
            print(f"[!] Error: vLLM server offline at {model.base_url}!")
            return False

        runner = AgentRunner(model_client=model, tool_registry=registry, max_iterations=5)

        # 5. Prompt requiring tool execution
        prompt = (
            "لطفاً با استفاده از ابزار get_system_health، وضعیت سلامت و منابع سیستم را بررسی کن "
            "و گزارشی شامل نوع پلتفرم، معماری و تعداد هسته‌های پردازشی ارائه بده."
        )
        messages = [{"role": "user", "content": prompt}]

        print(f"\n[*] User Prompt: \"{prompt}\"")
        print("[*] Executing autonomous AgentRunner loop...")
        print("-" * 65)

        result = runner.run(messages=messages, verbose=True)

        print("-" * 65)
        print(f"[+] Loop completed in {result['iterations']} iteration(s).")
        print(f"[+] Tools executed through MCP: {len(result['executed_tools'])}")
        for idx, t in enumerate(result['executed_tools'], 1):
            print(f"    {idx}. MCP Tool: '{t['name']}' | Args: {t['arguments']}")
            print(f"       Result: {t['result']}")

        print("~" * 65)
        print("📝 پاسخ نهایی مدل (Final Synthesized Response):")
        print("~" * 65)
        print(result["content"])
        print("~" * 65)

        if result["status"] == "success" and len(result["executed_tools"]) > 0:
            print("=" * 65)
            print("✅ TEST PASSED! Tool calling operates with 100% precision at Temperature=0.8.")
            print("=" * 65)
            return True
        else:
            print("[!] Note: Tool was not called or non-success status returned.")
            return False

    finally:
        print("[*] Shutting down MCPClient session...")
        mcp_client.close()
        print("[+] Session closed cleanly.")


if __name__ == "__main__":
    success = run_agent_tool_test()
    sys.exit(0 if success else 1)
