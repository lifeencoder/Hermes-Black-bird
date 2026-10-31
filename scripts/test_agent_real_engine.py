import sys
import os
import json
from pathlib import Path

for p in ["/marimo", "/marimo/model_package", "/marimo/hexstrike-ai"]:
    if p not in sys.path:
        sys.path.insert(0, p)

from client import ModelClient
from tools import ToolRegistry, MCPClient
from runner import AgentRunner

print("Initializing MCP Client with real hexstrike_mcp.py...")
mcp_client = MCPClient(
    command="/marimo/hexstrike-ai/venv/bin/python",
    args=["/marimo/hexstrike-ai/hexstrike_mcp.py"]
)

mcp_client.start()
registry = ToolRegistry()
registry.register_mcp_tools(mcp_client)
tool_names = registry.list_tool_names()
print(f"Total tools registered: {len(tool_names)}")

model_client = ModelClient(
    base_url="http://127.0.0.1:8000/v1",
    api_key="EMPTY",
    model_name="NousResearch/Hermes-3-Llama-3.1-70B-FP8",
    default_temperature=0.1,
    default_max_tokens=1024
)

runner = AgentRunner(
    model_client=model_client,
    tool_registry=registry,
    max_iterations=5
)

prompt = "با استفاده از ابزار execute_command، دستور whoami را اجرا کن."
print(f"\n--- Running Prompt: {prompt} ---")

def tool_callback(name, args, result):
    print(f"\n[TOOL CALL EXECUTED]")
    print(f"  Tool: {name}")
    print(f"  Args: {args}")
    print(f"  Result: {result}\n")

messages = [
    {
        "role": "system",
        "content": "You are Hermes AI Assistant. When instructed to use a specific tool, call that tool directly."
    },
    {
        "role": "user",
        "content": prompt
    }
]

result = runner.run(
    messages=messages,
    verbose=True,
    on_tool_call=tool_callback
)

print("\n=== FINAL AGENT RESULT ===")
print("Content:", result.get("content"))
print("Iterations:", result.get("iterations"))
print("Executed tools:", result.get("executed_tools"))

try:
    mcp_client.stop()
except Exception:
    pass
