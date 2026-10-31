import os
import sys
from pathlib import Path

# Set paths
sys.path.insert(0, "/marimo/model_package")
from client.model_client import ModelClient
from runner.agent_runner import AgentRunner
from tools.registry import ToolRegistry
from tools.mcp_client import MCPClient

print("=== TESTING REAL HERMES-3 70B + HEXSTRIKE ON MOLAB ===")
client = ModelClient(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY",
    model_name="NousResearch/Hermes-3-Llama-3.1-70B-FP8",
    default_temperature=0.2,
    default_top_p=0.95,
    default_presence_penalty=0.1,
    default_max_tokens=1024,
    default_system_prompt=(
        "You are an expert, highly capable, and objective engineering AI assistant. "
        "IMPORTANT: Always respond in fluent Persian (Farsi), even if tool outputs or technical data are in English. "
        "Translate and explain technical results in Persian for the user."
    )
)

mcp_client = MCPClient(
    command="/marimo/hexstrike-ai/venv/bin/python",
    args=["/marimo/hexstrike-ai/hexstrike_mcp.py"],
    startup_timeout=25.0
)
mcp_client.start()
registry = ToolRegistry()
registry.register_mcp_tools(mcp_client)
print(f"Loaded {len(registry.get_tools())} tools from HexStrike MCP")

runner = AgentRunner(model_client=client, tool_registry=registry, max_iterations=3)

prompt = "با استفاده از ابزار execute_command، دستور whoami را اجرا کن."
print(f"User Prompt: {prompt}")

messages = [{"role": "user", "content": prompt}]
result = runner.run(messages=messages)

print("\n=== FINAL AGENT RESPONSE ===")
print(result.get("response", "No response"))
print("\n=== TOOL CALLS EXECUTED ===")
print(result.get("tool_calls", []))
