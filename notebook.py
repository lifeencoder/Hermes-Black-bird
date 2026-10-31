# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "gdrive-fsspec==0.4.1",
#     "requests==2.34.2",
#     "marimo",
#     "openai",
#     "pyyaml",
# ]
# ///

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell(hide_code=True)
def env_check():
    import sys
    import os
    import json
    import shutil
    import subprocess
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def persian_chat_settings(mo):
    endpoint_url = mo.ui.text(
        value="http://localhost:8000/v1",
        label="🌐 آدرس سرور (Endpoint):",
        full_width=True
    )

    api_key = mo.ui.text(
        value="EMPTY",
        label="🔑 کلید دسترسی (API Key):",
        full_width=True
    )

    model_name = mo.ui.text(
        value="NousResearch/Hermes-3-Llama-3.1-70B-FP8",
        label="🤖 نام مدل (Model Name):",
        full_width=True
    )

    temperature = mo.ui.slider(
        start=0.0,
        stop=1.0,
        step=0.05,
        value=0.8,
        label="🌡️ دمای تولید (Temperature):",
        full_width=True
    )

    top_p = mo.ui.slider(
        start=0.1,
        stop=1.0,
        step=0.05,
        value=0.95,
        label="🎯 نمونه‌برداری هسته‌ای (Top-P):",
        full_width=True
    )

    presence_penalty = mo.ui.slider(
        start=0.0,
        stop=1.0,
        step=0.05,
        value=0.1,
        label="⚡ جریمه تکرار (Presence Penalty):",
        full_width=True
    )

    max_tokens = mo.ui.slider(
        start=256,
        stop=8192,
        step=256,
        value=2048,
        label="📊 حداکثر توکن (Max Tokens):",
        full_width=True
    )

    test_conn_btn = mo.ui.run_button(label="⚡ تست اتصال")
    clear_chat_btn = mo.ui.run_button(label="🗑️ پاک کردن چت")

    return (
        api_key,
        clear_chat_btn,
        endpoint_url,
        max_tokens,
        model_name,
        presence_penalty,
        temperature,
        test_conn_btn,
        top_p,
    )


@app.cell(hide_code=True)
def persian_chat_app():
    import os as _os
    import sys as _sys
    import marimo as _mo
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

    _header_md = _mo.md(
        f"### 🤖 دستیار هوشمند Hermes-3 (مقیاس‌پذیری {_tools_count} ابزار)\n"
        f"**وضعیت:** {_status_msg}"
    )

    _chat_ui = _mo.ui.chat(
        _chat_stream,
        prompts=[
            "با استفاده از ابزار execute_command، دستور whoami را اجرا کن.",
            "وضعیت سلامت سیستم را با ابزار get_system_health بررسی کن.",
            "مجموع اعداد ۱۲ و ۲۸ را با ابزار math_add حساب کن.",
            "تبدیل دمای ۳۷ درجه سانتی‌گراد به فارنهایت را با unit_celsius_to_fahrenheit انجام بده."
        ],
        max_height=520
    )

    return _mo.vstack([_header_md, _chat_ui])


if __name__ == "__main__":
    app.run()
