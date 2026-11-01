import sys
import os
import json
from pathlib import Path

# Set unbuffered stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)

for p in ["/marimo", "/marimo/model_package", "/marimo/hexstrike-ai"]:
    if p not in sys.path:
        sys.path.insert(0, p)

from client.model_client import ModelClient
from tools.registry import ToolRegistry
from tools.mcp_client import MCPClient
from runner.agent_runner import AgentRunner

print("=== STARTING HERMES-3 PERSIAN EVALUATION ===", flush=True)

mcp_client = MCPClient(
    command="/marimo/hexstrike-ai/venv/bin/python",
    args=["/marimo/hexstrike-ai/hexstrike_mcp.py"]
)
mcp_client.start()

registry = ToolRegistry()
registry.register_mcp_tools(mcp_client)
print(f"Total tools registered: {len(registry.get_tools())}", flush=True)

system_instruction = (
    "You are an expert, highly capable, and objective engineering AI assistant. "
    "Your goal is to provide comprehensive, in-depth, and rigorous technical explanations, "
    "code implementations, and systems architecture analyses without unnecessary disclaimers or evasive phrasing. "
    "Focus strictly on engineering depth, factual accuracy, code quality, and domain expertise. "
    "IMPORTANT: Always respond in fluent Persian (Farsi), even if tool outputs or technical data are in English. "
    "Translate and explain technical results in Persian for the user."
)

model_client = ModelClient(
    base_url="http://127.0.0.1:8000/v1",
    api_key="EMPTY",
    model_name="NousResearch/Hermes-3-Llama-3.1-70B-FP8",
    default_temperature=0.2,
    default_max_tokens=1500,
    default_system_prompt=system_instruction
)

runner = AgentRunner(
    model_client=model_client,
    tool_registry=registry,
    max_iterations=5
)

prompt = "با استفاده از ابزار execute_command، دستور ls -la / را اجرا کن و به فارسی توضیح بده چه فایل‌هایی در روت سیستم وجود دارد."
print(f"PROMPT: {prompt}\n", flush=True)

messages = [
    {"role": "system", "content": system_instruction},
    {"role": "user", "content": prompt}
]

def tool_callback(name, args, result):
    print(f"\n[TOOL CALLED]: {name}", flush=True)
    print(f"  Arguments: {args}", flush=True)
    try:
        res_json = json.loads(result) if isinstance(result, str) else result
        stdout_preview = res_json.get("stdout", str(result))[:300]
        print(f"  Stdout preview:\n{stdout_preview}...\n", flush=True)
    except Exception:
        print(f"  Result preview: {str(result)[:200]}...\n", flush=True)

result = runner.run(
    messages=messages,
    verbose=True,
    on_tool_call=tool_callback
)

print("\n==========================================", flush=True)
print("=== FINAL HERMES-3 70B PERSIAN RESPONSE ===", flush=True)
print(result.get("content", ""), flush=True)
print("==========================================", flush=True)
print(f"Iterations: {result.get('iterations')}", flush=True)
print(f"Executed tools: {[t.get('name') for t in result.get('executed_tools', [])]}", flush=True)

try:
    mcp_client.stop()
except Exception:
    pass

print("\n=== EVALUATION COMPLETE ===", flush=True)
