import marimo

app = marimo.App(width="medium")

@app.cell
def env_check():
    import sys
    import os
    import json
    import shutil
    import subprocess
    import marimo as mo
    return (mo,)

@app.cell
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

@app.cell
def persian_chat_app(
    api_key,
    clear_chat_btn,
    endpoint_url,
    max_tokens,
    mo,
    model_name,
    presence_penalty,
    temperature,
    test_conn_btn,
    top_p,
):
    import os as _os
    import sys as _sys
    from pathlib import Path as _Path
    import requests as _requests

    _ = clear_chat_btn.value
    _ = test_conn_btn.value

    _base_dir = _Path(__file__).resolve().parent if "__file__" in globals() else _Path.cwd()
    _repo_root = _base_dir.parent if _base_dir.name == "scripts" else _base_dir
    for _p in [_repo_root, _repo_root / "model_package", _Path("/marimo/model_package"), _base_dir]:
        if _p.exists() and str(_p) not in _sys.path:
            _sys.path.insert(0, str(_p))

    from client.model_client import ModelClient as _ModelClient
    from tools.registry import ToolRegistry as _ToolRegistry
    from tools.mcp_client import MCPClient as _MCPClient
    from runner.agent_runner import AgentRunner as _AgentRunner

    _mcp_candidates = [
        _Path("/marimo/model_package/tests/benchmark_150_tools_server.py"),
        _repo_root / "tests" / "benchmark_150_tools_server.py",
        _repo_root / "model_package" / "tests" / "benchmark_150_tools_server.py",
    ]
    _mcp_server_path = next((str(p) for p in _mcp_candidates if p.exists()), str(_repo_root / "tests" / "benchmark_150_tools_server.py"))

    _mcp_connected = False
    _mcp_tools_count = 0

    try:
        _mcp_client = _MCPClient(
            command=_sys.executable,
            args=[_mcp_server_path],
            startup_timeout=25.0
        )
        _mcp_client.start()
        _tool_registry = _ToolRegistry()
        _tool_registry.register_mcp_tools(_mcp_client)
        _mcp_connected = getattr(_mcp_client, "_is_connected", False)
        _mcp_tools_count = len(_tool_registry.get_tools())
    except Exception:
        _tool_registry = _ToolRegistry()

    _vllm_connected = False
    try:
        _res = _requests.get(f"{endpoint_url.value.rstrip('/')}/models", timeout=2)
        if _res.status_code == 200:
            _models = _res.json().get("data", [])
            _m_ids = [m.get("id") for m in _models]
            if model_name.value in _m_ids or len(_m_ids) > 0:
                _vllm_connected = True
    except Exception:
        pass

    _is_all_connected = _vllm_connected and _mcp_connected
    if _is_all_connected:
        _status_msg = f"متصل به سرور vLLM و رجیستری ابزارها ({_mcp_tools_count} ابزار فعال)"
    elif _mcp_connected:
        _status_msg = f"سرور ابزارها متصل ({_mcp_tools_count} ابزار) - سرور vLLM در انتظار اتصال"
    elif _vllm_connected:
        _status_msg = "متصل به سرور vLLM (ابزارهای محلی آفلاین)"
    else:
        _status_msg = "عدم برقراری ارتباط با سرورها"

    def hermes_chat_stream(messages, config):
        _client = _ModelClient(
            base_url=endpoint_url.value,
            api_key=api_key.value or "EMPTY",
            model_name=model_name.value,
            default_temperature=float(temperature.value),
            default_top_p=float(top_p.value),
            default_presence_penalty=float(presence_penalty.value),
            default_max_tokens=int(max_tokens.value)
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
                temperature=float(temperature.value),
                top_p=float(top_p.value),
                presence_penalty=float(presence_penalty.value),
                max_tokens=int(max_tokens.value)
            )
            if isinstance(_result, dict):
                yield _result.get("content", "پاسخی از مدل دریافت نشد.")
            else:
                yield str(_result)
        except Exception as _err:
            yield f"⚠️ **خطا در برقراری ارتباط با مدل:**\n\n`{str(_err)}`"

    _prompts = [
        "لطفاً با استفاده از ابزار execute_command، دستور whoami را اجرا کن.",
        "وضعیت سلامت سیستم را با ابزار get_system_health بررسی کن.",
        "مجموع اعداد ۱۲ و ۲۸ را با ابزار math_add حساب کن.",
        "تبدیل دمای ۳۷ درجه سانتی‌گراد به فارنهایت را با unit_celsius_to_fahrenheit انجام بده."
    ]

    chat_widget = mo.ui.chat(
        hermes_chat_stream,
        prompts=_prompts,
        max_height=560
    )

    _glass_css = """
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap');

    .glass-header-panel {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        padding: 18px 24px !important;
        background: rgba(255, 255, 255, 0.75) !important;
        backdrop-filter: blur(20px) saturate(190%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(190%) !important;
        border: 1px solid rgba(255, 255, 255, 0.9) !important;
        border-radius: 18px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.06) !important;
    }

    .glass-card-tool {
        background: linear-gradient(135deg, rgba(240, 249, 255, 0.85) 0%, rgba(224, 242, 254, 0.6) 100%) !important;
        border: 1px solid rgba(186, 230, 253, 0.8) !important;
        border-radius: 12px !important;
        padding: 12px 14px !important;
        font-size: 13px !important;
        line-height: 1.6 !important;
        color: #0369a1 !important;
    }

    .glass-badge {
        display: inline-flex !important;
        align-items: center !important;
        gap: 8px !important;
        padding: 6px 14px !important;
        border-radius: 9999px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(226, 232, 240, 0.8) !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03) !important;
    }

    @keyframes pulse-green-glow {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    @keyframes pulse-red-glow {
        0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
        70% { box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }

    .dot-green {
        width: 10px;
        height: 10px;
        background-color: #10b981;
        border-radius: 50%;
        display: inline-block;
        animation: pulse-green-glow 2s infinite;
    }
    .dot-red {
        width: 10px;
        height: 10px;
        background-color: #ef4444;
        border-radius: 50%;
        display: inline-block;
        animation: pulse-red-glow 2s infinite;
    }

    marimo-chatbot {
        direction: rtl !important;
        font-family: 'Vazirmatn', sans-serif !important;
    }
    marimo-chatbot textarea, marimo-chatbot input {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Vazirmatn', sans-serif !important;
        border-radius: 12px !important;
        border: 1px solid rgba(203, 213, 225, 0.8) !important;
        background: rgba(255, 255, 255, 0.9) !important;
    }
    """

    _style_block = mo.Html(f"<style>{_glass_css}</style>")

    _header = mo.Html(f"""
    <div class="glass-header-panel">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 44px; height: 44px; border-radius: 12px; background: linear-gradient(135deg, #0284c7, #0369a1); display: flex; align-items: center; justify-content: center; color: white; font-size: 24px; box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);">
                ✨
            </div>
            <div>
                <div style="font-size: 20px; font-weight: 800; color: #0f172a; letter-spacing: -0.3px;">دستیار هوشمند</div>
                <div style="font-size: 13px; color: #64748b; font-weight: 500;">عامل خودمختار و مدل زبانی Hermes-3 (Llama-3.1-70B FP8)</div>
            </div>
        </div>
        <div class="glass-badge" style="border-color: {'#a7f3d0' if _is_all_connected else '#fed7aa'}; background: {'rgba(236, 253, 245, 0.85)' if _is_all_connected else 'rgba(255, 247, 237, 0.85)'};">
            <span class="{'dot-green' if _is_all_connected else 'dot-red'}"></span>
            <span style="color: {'#065f46' if _is_all_connected else '#9a3412'};">{_status_msg}</span>
        </div>
    </div>
    """)

    _tool_preview_list = ", ".join(_tool_registry.list_tool_names()[:5]) if _mcp_tools_count > 0 else "ابزاری فعال نیست"

    _sidebar_panel = mo.vstack([
        mo.Html('<div style="font-size: 16px; font-weight: 800; color: #0f172a; border-bottom: 2px solid rgba(226, 232, 240, 0.8); padding-bottom: 10px; margin-bottom: 14px; display: flex; align-items: center; gap: 8px;">⚙️ تنظیمات مدل و استنتاج</div>'),
        endpoint_url,
        api_key,
        model_name,
        temperature,
        top_p,
        presence_penalty,
        max_tokens,
        mo.Html("<hr style='border: none; border-top: 1px solid rgba(226, 232, 240, 0.8); margin: 10px 0;'/>"),
        mo.Html(f"""
        <div class="glass-card-tool">
            <div style="font-weight: 700; margin-bottom: 4px; display: flex; align-items: center; gap: 6px;">
                <span>🛠️</span>
                <span>سرور ابزارهای محلی ({_mcp_tools_count} ابزار فعال)</span>
            </div>
            <div style="font-size: 11px; color: #0284c7; font-family: monospace; direction: ltr; text-align: left; background: rgba(255,255,255,0.7); padding: 4px 8px; border-radius: 6px; margin-top: 4px;">
                {_tool_preview_list}...
            </div>
        </div>
        """),
        mo.Html("<div style='height: 4px;'></div>"),
        mo.hstack([test_conn_btn, clear_chat_btn], justify="space-between"),
        mo.Html("""
        <div style="font-size: 12px; color: #475569; line-height: 1.6; margin-top: 12px; background: rgba(248, 250, 252, 0.7); padding: 10px 14px; border-radius: 10px; border: 1px solid rgba(226, 232, 240, 0.8);">
            💡 <b>راهنما:</b> تمام مقادیر اسلایدرها به صورت بلادرنگ به مدل ارسال می‌شوند و پیام‌ها وارد چرخه خودکار ابزارها می‌گردند.
        </div>
        """)
    ], gap=0.8).style({
        "background": "rgba(255, 255, 255, 0.65)",
        "backdrop-filter": "blur(16px)",
        "-webkit-backdrop-filter": "blur(16px)",
        "border": "1px solid rgba(255, 255, 255, 0.8)",
        "border-radius": "18px",
        "padding": "20px",
        "width": "340px",
        "min-width": "320px",
        "box-shadow": "0 8px 32px 0 rgba(31, 38, 135, 0.05)"
    })

    _chat_panel = mo.vstack([
        chat_widget
    ]).style({
        "background": "rgba(255, 255, 255, 0.7)",
        "backdrop-filter": "blur(16px)",
        "-webkit-backdrop-filter": "blur(16px)",
        "border": "1px solid rgba(255, 255, 255, 0.8)",
        "border-radius": "18px",
        "padding": "16px",
        "flex": "1",
        "min-width": "460px",
        "box-shadow": "0 8px 32px 0 rgba(31, 38, 135, 0.05)"
    })

    _main_layout = mo.vstack([
        _style_block,
        _header,
        mo.hstack([
            _sidebar_panel,
            _chat_panel
        ], gap=1.2)
    ], gap=1).style({
        "direction": "rtl",
        "text-align": "right",
        "font-family": "'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "background": "linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 50%, #f8fafc 100%)",
        "padding": "24px",
        "border-radius": "24px",
        "border": "1px solid rgba(255, 255, 255, 0.8)",
        "box-shadow": "0 20px 40px -15px rgba(0, 0, 0, 0.05)"
    })

    _main_layout
    return

if __name__ == "__main__":
    app.run()
