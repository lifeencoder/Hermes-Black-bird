import sys
sys.path.insert(0, '/marimo/model_package')
from client.model_client import ModelClient
from runner.agent_runner import AgentRunner
from tools.registry import ToolRegistry
from tools.mcp_client import MCPClient

client = ModelClient(
    base_url='http://localhost:8000/v1',
    api_key='EMPTY',
    model_name='NousResearch/Hermes-3-Llama-3.1-70B-FP8',
    default_temperature=0.2,
    default_system_prompt='You are an expert AI assistant. Always respond in fluent Persian (Farsi).'
)
mcp = MCPClient('/marimo/hexstrike-ai/venv/bin/python', ['/marimo/hexstrike-ai/hexstrike_mcp.py'])
mcp.start()
reg = ToolRegistry()
reg.register_mcp_tools(mcp)

runner = AgentRunner(client, reg, max_iterations=3)
r = runner.run([{'role': 'user', 'content': 'با استفاده از ابزار execute_command، دستور whoami را اجرا کن.'}])

with open('/marimo/test_output.txt', 'w', encoding='utf-8') as f:
    f.write("=== FINAL PERSIAN RESPONSE ===\n")
    f.write(r['content'] + "\n\n")
    f.write("=== EXECUTED TOOLS ===\n")
    for t in r['executed_tools']:
        f.write(f"Tool: {t['name']}\nArgs: {t['arguments']}\nResult: {t['result']}\n\n")

print("Finished writing test output to /marimo/test_output.txt")
