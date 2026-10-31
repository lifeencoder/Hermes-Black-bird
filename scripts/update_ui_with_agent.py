import marimo._code_mode as cm

new_bkhc_code = '''import importlib
import requests as _requests

# وابستگی به دکمه‌های کنترل
_ = clear_chat_btn.value
_ = test_conn_btn.value

if "/marimo/model_package" not in sys.path:
    sys.path.insert(0, "/marimo/model_package")

import client.model_client
import runner.agent_runner
importlib.reload(client.model_client)
importlib.reload(runner.agent_runner)

from client.model_client import ModelClient as _ModelClient
from tools.registry import ToolRegistry as _ToolRegistry
from tools.mcp_client import MCPClient as _MCPClient
from runner.agent_runner import AgentRunner as _AgentRunner

with open("/marimo/custom.css", "r", encoding="utf-8") as _f:
    _custom_css = _f.read()

_style_block = mo.Html(f"<style>{_custom_css}</style>")

# مقداردهی و اتصال به سرور محلی MCP
_mcp_server_script = "/marimo/model_package/tests/mock_custom_mcp.py"
_mcp_connected = False
_mcp_tools_count = 0

try:
    if "_mcp_client" in globals() and _mcp_client is not None:
        try:
            _mcp_client.close()
        except Exception:
            pass
    _mcp_client = _MCPClient(
        command=sys.executable,
        args=[_mcp_server_script],
        startup_timeout=20.0
    )
    _mcp_client.start()
    _tool_registry = _ToolRegistry()
    _tool_registry.register_mcp_tools(_mcp_client)
    _mcp_connected = getattr(_mcp_client, "_is_connected", False)
    _mcp_tools_count = len(_tool_registry.list_tool_names())
except Exception as _mcp_err:
    print(f"MCP init error: {_mcp_err}")
    _tool_registry = _ToolRegistry()

# بررسی اتصال مدل vLLM
_vllm_connected = False
try:
    _res = _requests.get(f"{endpoint_url.value.rstrip('/')}/models", timeout=3)
    if _res.status_code == 200:
        _models = _res.json().get("data", [])
        _m_ids = [m["id"] for m in _models]
        if model_name.value in _m_ids:
            _vllm_connected = True
except Exception:
    pass

_is_all_connected = _vllm_connected and _mcp_connected
if _is_all_connected:
    _status_msg = f"متصل به سرور vLLM و MCP ({_mcp_tools_count} ابزار فعال)"
elif _vllm_connected:
    _status_msg = "متصل به سرور vLLM (ابزارهای MCP آفلاین)"
else:
    _status_msg = "عدم برقراری ارتباط با سرور"

def hermes_chat_stream(messages, config):
    _client = _ModelClient(
        base_url=endpoint_url.value,
        api_key=api_key.value or "EMPTY",
        model_name=model_name.value,
        default_temperature=temperature.value,
        default_top_p=top_p.value,
        default_presence_penalty=presence_penalty.value,
        default_max_tokens=max_tokens.value
    )
    _runner = _AgentRunner(
        model_client=_client,
        tool_registry=_tool_registry,
        max_iterations=5
    )
    _api_messages = []
    for _msg in messages:
        _role = getattr(_msg, "role", "user")
        _content = getattr(_msg, "content", "")
        if _content:
            _api_messages.append({"role": _role, "content": str(_content)})

    try:
        _result = _runner.run(
            messages=_api_messages,
            verbose=False,
            temperature=temperature.value,
            top_p=top_p.value,
            presence_penalty=presence_penalty.value,
            max_tokens=max_tokens.value
        )
        if isinstance(_result, dict):
            yield _result.get("content", "")
        else:
            yield str(_result)
    except Exception as _err:
        yield f"⚠️ **خطا در چرخه اجرای عامل هوشمند:**\\n\\n`{str(_err)}`\\n\\nلطفاً از فعال بودن سرورها اطمینان حاصل کنید."

_prompts = [
    "با استفاده از ابزار execute_command، دستور 'echo Hello' را اجرا کن.",
    "با استفاده از ابزار get_system_health، وضعیت و سلامت سیستم را گزارش بده.",
    "با استفاده از ابزار echo_message، پیام 'Hermes UI Agent Ping' را به سرور MCP بفرست.",
    "تعداد کلمات و کاراکترهای متن 'هوش مصنوعی زاینده' را با ابزار count_text_stats حساب کن."
]

chat_widget = mo.ui.chat(
    hermes_chat_stream,
    prompts=_prompts,
    max_height=580
)

_header = mo.Html(f"""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 14px 20px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; margin-bottom: 14px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04); font-family: 'Vazirmatn', sans-serif;">
    <div style="font-size: 19px; font-weight: 800; color: #0f172a; display: flex; align-items: center; gap: 8px;">
        <span style="color: #0284c7; font-size: 22px;">✨</span>
        <span>دستیار هوشمند و عامل خودمختار Hermes-3 (Llama-3.1-70B FP8)</span>
    </div>
    <div style="display: inline-flex; align-items: center; gap: 8px; padding: 6px 14px; border-radius: 9999px; font-size: 13px; font-weight: 600; background: {'#ecfdf5' if _is_all_connected else '#fef2f2'}; border: 1px solid {'#a7f3d0' if _is_all_connected else '#fecaca'};">
        <span class="{'status-dot-green' if _is_all_connected else 'status-dot-red'}"></span>
        <span style="color: {'#065f46' if _is_all_connected else '#991b1b'};">{_status_msg}</span>
    </div>
</div>
""")

_tool_names_preview = ", ".join(_tool_registry.list_tool_names()[:5]) if _mcp_tools_count > 0 else "هیچ ابزاری فعال نیست"

_sidebar_panel = mo.vstack([
    mo.Html('<div style="font-size: 15px; font-weight: 700; color: #0f172a; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; margin-bottom: 12px; display: flex; align-items: center; gap: 6px; font-family: \\'Vazirmatn\\', sans-serif;">⚙️ تنظیمات مدل و عامل هوشمند</div>'),
    endpoint_url,
    api_key,
    model_name,
    temperature,
    top_p,
    presence_penalty,
    max_tokens,
    mo.Html("<hr style='border-color: #e2e8f0; margin: 8px 0;'/>"),
    mo.Html(f"""
    <div style="font-size: 12px; color: #0369a1; background: #f0f9ff; padding: 8px 12px; border-radius: 8px; border: 1px solid #bae6fd; font-family: 'Vazirmatn', sans-serif; line-height: 1.5;">
        🛠️ <b>ابزارهای محلی MCP ({_mcp_tools_count}):</b><br/>
        <span style="font-family: monospace; font-size: 11px;">{_tool_names_preview}...</span>
    </div>
    """),
    mo.hstack([test_conn_btn, clear_chat_btn], justify="space-between"),
    mo.Html("""
    <div style="font-size: 12px; color: #475569; line-height: 1.6; margin-top: 10px; background: #f8fafc; padding: 8px 12px; border-radius: 8px; border: 1px solid #e2e8f0; font-family: 'Vazirmatn', sans-serif;">
        💡 <b>راهنما:</b> پیام‌های ارسالی وارد حلقه خودکار AgentRunner می‌شوند و مدل می‌تواند مستقیماً ابزارها را فراخوانی کند.
    </div>
    """)
], gap=0.8).style({
    "background": "#ffffff",
    "border": "1px solid #e2e8f0",
    "border-radius": "12px",
    "padding": "16px",
    "width": "320px",
    "min-width": "300px",
    "box-shadow": "0 1px 3px rgba(0, 0, 0, 0.04)"
})

_chat_panel = mo.vstack([
    chat_widget
]).style({
    "background": "#ffffff",
    "border": "1px solid #e2e8f0",
    "border-radius": "12px",
    "padding": "14px",
    "flex": "1",
    "min-width": "460px",
    "box-shadow": "0 1px 3px rgba(0, 0, 0, 0.04)"
})

persian_chat_app_view = mo.vstack([
    _style_block,
    _header,
    mo.hstack([_sidebar_panel, _chat_panel], gap=1.2)
], gap=1).style({
    "direction": "rtl",
    "font-family": "'Vazirmatn', sans-serif",
    "background": "#f8fafc",
    "border": "1px solid #e2e8f0",
    "border-radius": "16px",
    "padding": "20px",
    "box-shadow": "0 4px 20px -2px rgba(0, 0, 0, 0.05)"
})

persian_chat_app_view'''

async with cm.get_context(skip_staleness_check=True) as ctx:
    ctx.edit_cell("bkHC", code=new_bkhc_code)
    ctx.run_cell("bkHC")

print("[✓] Updated bkHC: yields result.get('content', '') cleanly without raw JSON dictionaries.")
