#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hermes Black Bird - Generic MCP Server Discovery & Registry Tester
A dynamic, server-agnostic verification utility. Accepts any standard MCP server
script via command-line arguments, connects over stdio, performs tool discovery,
and verifies seamless registration in ToolRegistry.
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

from tools.mcp_client import MCPClient
from tools.registry import ToolRegistry


def run_generic_test(server_path: str):
    server_file = Path(server_path).resolve()
    print("=" * 70)
    print("🦅 Hermes Black Bird - Generic MCP Server Discovery & Registration")
    print("=" * 70)
    print(f"[*] Target Server Script:  {server_file}")
    print(f"[*] Python Interpreter:    {sys.executable}")

    if not server_file.exists():
        print(f"[!] ERROR: Target server script not found: {server_file}")
        sys.exit(1)

    # 1. Connect via MCPClient over stdio
    print("\n[*] Initializing MCPClient over stdio...")
    client = MCPClient(
        command=sys.executable,
        args=[str(server_file)],
        startup_timeout=20.0,
    )

    try:
        client.start()
        print("[+] Successfully connected to the MCP Server process!")

        # 2. Discover Tools
        print("[*] Performing Tools Discovery (list_tools)...")
        discovered_tools = client.list_tools()
        tools_count = len(discovered_tools)
        print(f"[+] Total tools discovered: {tools_count}")
        print("-" * 70)

        # 3. Print discovered tools table
        print(f"{'#':<3} | {'Tool Name':<28} | {'Params':<6} | Description")
        print("-" * 70)
        for idx, tool in enumerate(discovered_tools, 1):
            name = tool["name"]
            params = tool.get("parameters", {}).get("properties", {})
            param_count = len(params)
            desc = tool.get("description", "").strip().replace("\n", " ")
            if len(desc) > 35:
                desc = desc[:32] + "..."
            print(f"{idx:<3} | {name:<28} | {param_count:<6} | {desc}")

        print("-" * 70)

        # 4. Ingest and register tools into ToolRegistry
        print("[*] Registering discovered tools into ToolRegistry...")
        registry = ToolRegistry()
        registered_names = registry.register_mcp_tools(client)
        registry_count = len(registered_names)
        print(f"[+] Successfully registered {registry_count} tools into ToolRegistry.")

        # 5. Verify round-trip execution on a sample tool
        sample_tool = None
        for candidate in ["echo_message", "get_system_health", "generate_uuid", registered_names[0]]:
            if candidate in registered_names:
                sample_tool = candidate
                break

        if sample_tool:
            print(f"\n[*] Executing sample round-trip call to '{sample_tool}'...")
            test_args = {"message": "Hermes Generic Tester Ping"} if sample_tool == "echo_message" else {}
            exec_result = registry.execute(sample_tool, test_args)
            preview = exec_result[:150] + ("..." if len(exec_result) > 150 else "")
            print(f"[+] Response from '{sample_tool}':\n    {preview}")

        # 6. Final verification
        if registry_count == tools_count and registry_count > 0:
            print("\n" + "=" * 70)
            print(f"✅ GENERIC MCP TEST PASSED! All {registry_count} tools registered and operational.")
            print("=" * 70)
            return True
        else:
            print(f"[!] Mismatch: Discovered {tools_count} vs Registered {registry_count}")
            return False

    finally:
        print("[*] Terminating MCP server process...")
        client.close()
        print("[+] Session closed cleanly.")


def main():
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        # Default fallback to mock_custom_mcp.py
        target = str(Path(__file__).resolve().parent / "mock_custom_mcp.py")
        print(f"[*] No server argument specified. Defaulting to: {target}")

    success = run_generic_test(target)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
