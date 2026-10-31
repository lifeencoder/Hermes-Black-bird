import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

if "/marimo/model_package" not in sys.path:
    sys.path.insert(0, "/marimo/model_package")

from client.model_client import ModelClient
from tools.registry import ToolRegistry
from tools.mcp_client import MCPClient
from runner.agent_runner import AgentRunner

mcp_path = "/marimo/model_package/tests/benchmark_150_tools_server.py"

print("=================================================================")
print("🦅 Testing Scalability Benchmark Agent (160+ Tools Suite)")
print("=================================================================")

print("[*] Connecting to MCP Server...")
mcp = MCPClient(command=sys.executable, args=[mcp_path], startup_timeout=25.0)
mcp.start()

registry = ToolRegistry()
registry.register_mcp_tools(mcp)
total_tools = len(registry.get_tools())
print(f"✅ Total Discovered Tools: {total_tools}")

prompt = "با استفاده از ابزار execute_command، دستور whoami را اجرا کن."
print(f"[*] Prompt: \"{prompt}\"")
print("[*] Running AgentRunner...")

client = ModelClient()
runner = AgentRunner(model_client=client, tool_registry=registry, max_iterations=5)

result = runner.run(
    messages=[{"role": "user", "content": prompt}],
    verbose=True
)

print("\n" + "=" * 65)
print(f"📊 گزارش تعداد ابزارهای کشف‌شده: {total_tools} ابزار (بیشتر از ۱۵۰)")
print("=" * 65)
print("📝 خروجی نهایی مدل در چت‌باکس:")
print(result.get("content", ""))
print("=" * 65)
print(f"🔧 ابزارهای فراخوانی‌شده: {result.get('executed_tools')}")
print("=" * 65)

mcp.close()
