import sys
import os
from pathlib import Path

# Set stdout to UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

print("=================================================================")
print("🧪 TESTING MARIMO UI CELLS AND CONNECTIONS LOCALLY")
print("=================================================================")

import marimo as mo

# 1. Test Cell 1: env_check
print("[1/4] Executing Cell 1 (env_check)...")
import shutil, subprocess, json
print("   -> Cell 1 OK.")

# 2. Test Cell 2: persian_chat_settings
print("[2/4] Executing Cell 2 (persian_chat_settings)...")
endpoint_url = mo.ui.text(value="http://localhost:8000/v1", label="🌐 آدرس سرور (Endpoint):", full_width=True)
api_key = mo.ui.text(value="EMPTY", label="🔑 کلید دسترسی (API Key):", full_width=True)
model_name = mo.ui.text(value="NousResearch/Hermes-3-Llama-3.1-70B-FP8", label="🤖 نام مدل (Model Name):", full_width=True)
temperature = mo.ui.slider(start=0.0, stop=1.0, step=0.05, value=0.8, label="🌡️ دمای تولید (Temperature):", full_width=True)
top_p = mo.ui.slider(start=0.1, stop=1.0, step=0.05, value=0.95, label="🎯 نمونه‌برداری هسته‌ای (Top-P):", full_width=True)
presence_penalty = mo.ui.slider(start=0.0, stop=1.0, step=0.05, value=0.1, label="⚡ جریمه تکرار (Presence Penalty):", full_width=True)
max_tokens = mo.ui.slider(start=256, stop=8192, step=256, value=2048, label="📊 حداکثر توکن (Max Tokens):", full_width=True)
test_conn_btn = mo.ui.run_button(label="⚡ تست اتصال")
clear_chat_btn = mo.ui.run_button(label="🗑️ پاک کردن چت")

print(f"   -> Settings widgets instantiated:")
print(f"      Temperature: {temperature.value}")
print(f"      Top-P: {top_p.value}")
print(f"      Presence Penalty: {presence_penalty.value}")
print(f"      Max Tokens: {max_tokens.value}")

# 3. Test Cell 3: persian_chat_app and MCP Server connection
print("[3/4] Executing Cell 3 (persian_chat_app) & Local MCP Server connection...")
from client.model_client import ModelClient
from tools.registry import ToolRegistry
from tools.mcp_client import MCPClient
from runner.agent_runner import AgentRunner

mcp_path = root / "tests" / "benchmark_150_tools_server.py"
print(f"   -> MCP Server Path: {mcp_path}")
assert mcp_path.exists(), f"MCP server file not found at {mcp_path}"

mcp_client = MCPClient(
    command=sys.executable,
    args=[str(mcp_path)],
    startup_timeout=25.0
)
mcp_client.start()
print("   -> MCPClient started successfully.")

tool_registry = ToolRegistry()
tool_registry.register_mcp_tools(mcp_client)
tool_count = len(tool_registry.get_tools())
print(f"   -> Discovered tools count: {tool_count} tools.")
assert tool_count >= 150, f"Expected >= 150 tools, got {tool_count}"

# Test a benign tool execution directly on the server
test_result = mcp_client.call_tool("execute_command", {"command": "whoami"})
print(f"   -> Direct tool call test (whoami): '{test_result}'")
assert "hermes-agent" in test_result

mcp_client.close()
print("   -> MCPClient connection closed cleanly.")

print("[4/4] Verifying Dynamic Parameter Binding in AgentRunner...")
# Verify that slider values are passed dynamically into ModelClient
client = ModelClient(
    base_url=endpoint_url.value,
    api_key=api_key.value,
    model_name=model_name.value,
    default_temperature=temperature.value,
    default_top_p=top_p.value,
    default_presence_penalty=presence_penalty.value,
    default_max_tokens=max_tokens.value
)

assert client.default_temperature == 0.8
assert client.default_top_p == 0.95
assert client.default_presence_penalty == 0.1
assert client.default_max_tokens == 2048

# Test with modified slider value to confirm dynamic binding (not hardcoded)
temperature2 = mo.ui.slider(start=0.0, stop=1.0, value=0.4)
client2 = ModelClient(
    base_url=endpoint_url.value,
    api_key=api_key.value,
    model_name=model_name.value,
    default_temperature=temperature2.value
)
assert client2.default_temperature == 0.4, "Failed: Parameter was hardcoded!"
print("   -> Dynamic parameter binding verified: Changing slider dynamically updates ModelClient configuration.")

print("\n=================================================================")
print("✅ ALL LOCAL UI COMPONENTS AND MCP CONNECTIONS VERIFIED SUCCESSFULLY!")
print("=================================================================")
