import marimo._code_mode as cm

new_cell_code = '''import marimo as _mo
import sys as _sys
import os as _os
import importlib as _importlib

if "/marimo/model_package" not in _sys.path:
    _sys.path.insert(0, "/marimo/model_package")

import client.model_client as _cmc
import runner.agent_runner as _rar
_importlib.reload(_cmc)
_importlib.reload(_rar)

from client.model_client import ModelClient as _ModelClient
from tools.registry import ToolRegistry as _ToolRegistry
from tools.mcp_client import MCPClient as _MCPClient
from runner.agent_runner import AgentRunner as _AgentRunner

# مسیر سرور ابزارهای کامل (۱۶۵ ابزار بنچمارک مقیاس‌پذیری)
_mcp_path = "/marimo/model_package/tests/benchmark_150_tools_server.py"

try:
    if "_mcp" in globals() and _mcp is not None:
        try:
            _mcp.close()
        except Exception:
            pass
    _mcp = _MCPClient(command=_sys.executable, args=[_mcp_path], startup_timeout=25.0)
    _mcp.start()
    _registry = _ToolRegistry()
    _registry.register_mcp_tools(_mcp)
    _tools_count = len(_registry.get_tools())
    _status_msg = f"🟢 متصل به {_tools_count} ابزار (موتور مقیاس‌پذیری)"
except Exception as _e:
    _tools_count = 0
    _status_msg = f"🔴 خطا در اتصال به ابزارها: {str(_e)[:50]}"

def _chat_stream(messages, config):
    _client = _ModelClient()
    _runner = _AgentRunner(model_client=_client, tool_registry=_registry, max_iterations=5)
    
    _api_msgs = []
    for _m in messages:
        _role = getattr(_m, "role", "user")
        _content = getattr(_m, "content", "")
        if _content:
            _api_msgs.append({"role": _role, "content": str(_content)})

    try:
        _result = _runner.run(messages=_api_msgs, verbose=False)
        if isinstance(_result, dict):
            yield _result.get("content", "پاسخی دریافت نشد.")
        else:
            yield str(_result)
    except Exception as _err:
        yield f"❌ خطا در اجرای مدل: {str(_err)}"

# رابط کاربری
_header_md = _mo.md(f"### 🤖 دستیار هوشمند Hermes-3 (مقیاس‌پذیری {_tools_count} ابزار)\\n**وضعیت:** {_status_msg}")

_chat_ui = _mo.ui.chat(
    _chat_stream,
    prompts=[
        "با استفاده از ابزار execute_command، دستور whoami را اجرا کن.",
        "وضعیت سلامت سیستم را با ابزار get_system_health بررسی کن.",
        "مجموع اعداد ۱۲ و ۲۸ را با ابزار math_add حساب کن."
    ],
    max_height=520
)

_mo.vstack([_header_md, _chat_ui])'''

async with cm.get_context(skip_staleness_check=True) as ctx:
    if "oulP" in ctx.cells:
        ctx.delete_cell("oulP")
        print("[✓] Cleaned up oulP.")
    if "bkHC" in ctx.cells:
        ctx.edit_cell("bkHC", code=new_cell_code)
        ctx.run_cell("bkHC")
        print("[✓] Updated cell bkHC with new clean UI and ran successfully.")
    else:
        new_id = ctx.create_cell(code=new_cell_code)
        ctx.run_cell(new_id)
        print(f"[✓] Created new cell {new_id} and ran successfully.")
