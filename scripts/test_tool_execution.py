import sys
import os
import json
from pathlib import Path

for p in ["/marimo", "/marimo/model_package", "/marimo/hexstrike-ai"]:
    if p not in sys.path:
        sys.path.insert(0, p)

from client.model_client import ModelClient
from tools.registry import ToolRegistry
from tools.mcp_client import MCPClient
from runner.agent_runner import AgentRunner

mcp_client = MCPClient(
    command="/marimo/hexstrike-ai/venv/bin/python",
    args=["/marimo/hexstrike-ai/hexstrike_mcp.py"]
)
mcp_client.start()
registry = ToolRegistry()
registry.register_mcp_tools(mcp_client)

sys_prompt = (
    "You are an expert, highly capable, and objective engineering AI assistant. "
    "Your goal is to provide comprehensive, in-depth, and rigorous technical explanations, "
    "code implementations, and systems architecture analyses without unnecessary disclaimers or evasive phrasing. "
    "Focus strictly on engineering depth, factual accuracy, code quality, and domain expertise. "
    "When instructed to use a tool or execute a command, invoke the corresponding tool call directly. "
    "IMPORTANT: Always respond in fluent Persian (Farsi), even if tool outputs or technical data are in English. "
    "Translate and explain technical results in Persian for the user."
)

client = ModelClient(
    base_url="http://127.0.0.1:8000/v1",
    api_key="EMPTY",
    model_name="NousResearch/Hermes-3-Llama-3.1-70B-FP8",
    default_temperature=0.1,
    default_max_tokens=2048,
    default_system_prompt=sys_prompt
)

runner = AgentRunner(model_client=client, tool_registry=registry, max_iterations=5)

prompt = "با استفاده از ابزار execute_command، دستور ls -la / را اجرا کن و به فارسی توضیح بده چه فایلهایی در روت سیستم وجود دارد."

def tool_cb(name, args, res):
    print(f"\n[TOOL EXECUTED]: {name}")
    print(f"ARGS: {args}")
    try:
        r = json.loads(res) if isinstance(res, str) else res
        print(f"STDOUT: {r.get('stdout', '')[:400]}")
    except Exception:
        print(f"RES: {str(res)[:200]}")

res = runner.run(
    messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": prompt}],
    verbose=True,
    on_tool_call=tool_cb
)

print("\n=== FINAL PERSIAN RESPONSE ===")
print(res.get("content"))
print("================================")
print("EXECUTED TOOLS:", [t.get("name") for t in res.get("executed_tools", [])])

try:
    mcp_client.stop()
except Exception:
    pass
