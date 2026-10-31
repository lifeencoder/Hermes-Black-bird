import sys
import os
import time
import json
import requests

print(">>> Starting live test on MoLab...", flush=True)

# 1. Wait for vLLM to be ready
print("Waiting for vLLM server on port 8000...", flush=True)
for i in range(60):
    try:
        r = requests.get("http://127.0.0.1:8000/v1/models", timeout=2)
        if r.status_code == 200:
            print("vLLM server is READY! Models:", r.json(), flush=True)
            break
    except Exception:
        pass
    time.sleep(2)
else:
    print("Error: vLLM server did not become ready in 120s", flush=True)
    sys.exit(1)

# 2. Add packages to sys.path
for p in ["/marimo", "/marimo/model_package", "/marimo/hexstrike-ai"]:
    if p not in sys.path:
        sys.path.insert(0, p)

from client import ModelClient
from tools import ToolRegistry, MCPClient
from runner import AgentRunner

print("Initializing MCP Client with real hexstrike_mcp.py...", flush=True)
mcp_client = MCPClient(
    command="/marimo/hexstrike-ai/venv/bin/python",
    args=["/marimo/hexstrike-ai/hexstrike_mcp.py"]
)
mcp_client.start()

registry = ToolRegistry()
registry.register_mcp_tools(mcp_client)
tool_names = registry.list_tool_names()
print(f"Total tools registered in ToolRegistry: {len(tool_names)}", flush=True)
print(f"Does registry contain 'execute_command'? {'execute_command' in tool_names}", flush=True)

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
print(f"\n==========================================", flush=True)
print(f"PROMPT: {prompt}", flush=True)
print(f"==========================================\n", flush=True)

executed_tool_details = []

def tool_callback(name, args, result):
    executed_tool_details.append({
        "name": name,
        "args": args,
        "result": result
    })
    print(f"\n[TOOL CALLED BY MODEL]: {name}", flush=True)
    print(f"  Arguments: {args}", flush=True)
    print(f"  Result: {result}", flush=True)

messages = [
    {
        "role": "system",
        "content": "You are Hermes AI Assistant. When instructed to use a specific tool, invoke that tool directly."
    },
    {
        "role": "user",
        "content": prompt
    }
]

res = runner.run(
    messages=messages,
    verbose=True,
    on_tool_call=tool_callback
)

print("\n==========================================", flush=True)
print("=== FINAL RESULT FROM HERMES-3 70B ===", flush=True)
print(f"Final Content: {res.get('content')}", flush=True)
print(f"Iterations: {res.get('iterations')}", flush=True)
print(f"Executed Tools List: {res.get('executed_tools')}", flush=True)
print("Tool Execution Details:", json.dumps(executed_tool_details, ensure_ascii=False, indent=2), flush=True)
print("==========================================", flush=True)

try:
    mcp_client.stop()
except Exception:
    pass

print(">>> Test completed successfully!", flush=True)
