import subprocess
import json

py = "/marimo/hexstrike-ai/venv/bin/python"
mcp = "/marimo/hexstrike-ai/hexstrike_mcp.py"

print("Testing HexStrike MCP tools listing:")
init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}) + "\n"
tools_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}) + "\n"

proc = subprocess.Popen([py, mcp], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
stdout, stderr = proc.communicate(input=init_req + tools_req, timeout=10)
print("Stderr:", stderr[:300])
lines = stdout.strip().split("\n")
print(f"Stdout lines received: {len(lines)}")
for l in lines:
    try:
        data = json.loads(l)
        if "result" in data and "tools" in data["result"]:
            print(f"Total tools returned: {len(data['result']['tools'])}")
            print("First 3 tools:", [t["name"] for t in data["result"]["tools"][:3]])
    except Exception as e:
        pass
