# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "gdrive-fsspec==0.4.1",
#     "requests==2.34.2",
#     "marimo",
#     "openai",
#     "pyyaml",
#     "mcp",
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
        label="آدرس سرور استنتاج (Endpoint)",
        full_width=True
    )
    api_key = mo.ui.text(
        value="EMPTY",
        label="کلید دسترسی (API Key)",
        full_width=True
    )
    model_name = mo.ui.text(
        value="NousResearch/Hermes-3-Llama-3.1-70B-FP8",
        label="شناسه مدل (Model Name)",
        full_width=True
    )
    temperature = mo.ui.slider(
        start=0.0,
        stop=1.0,
        step=0.05,
        value=0.8,
        label="دمای تولید (Temperature)",
        full_width=True
    )
    top_p = mo.ui.slider(
        start=0.1,
        stop=1.0,
        step=0.05,
        value=0.95,
        label="نمونه‌برداری هسته‌ای (Top-P)",
        full_width=True
    )
    presence_penalty = mo.ui.slider(
        start=0.0,
        stop=1.0,
        step=0.05,
        value=0.1,
        label="جریمه تکرار توکن (Presence Penalty)",
        full_width=True
    )
    max_tokens = mo.ui.slider(
        start=256,
        stop=8192,
        step=256,
        value=2048,
        label="حداکثر توکن تولیدی (Max Tokens)",
        full_width=True
    )
    test_conn_btn = mo.ui.run_button(label="آزمون اتصال")
    clear_chat_btn = mo.ui.run_button(label="پاک‌سازی گفتگو")

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
    import base64 as _base64
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
        _Path("/marimo/hexstrike-ai/hexstrike_mcp.py"),
        _Path("/marimo/model_package/tests/benchmark_150_tools_server.py"),
        _repo_root / "tests" / "benchmark_150_tools_server.py",
        _repo_root / "model_package" / "tests" / "benchmark_150_tools_server.py",
    ]
    _mcp_server_path = next((str(p) for p in _mcp_candidates if p.exists()), "/marimo/hexstrike-ai/hexstrike_mcp.py")

    _hexstrike_venv_py = _Path("/marimo/hexstrike-ai/venv/bin/python")
    _mcp_py_cmd = str(_hexstrike_venv_py) if _hexstrike_venv_py.exists() else _sys.executable

    _mcp_connected = False
    _mcp_tools_count = 0

    try:
        _mcp_client = _MCPClient(
            command=_mcp_py_cmd,
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
        _system_instruction = (
            "You are an expert, highly capable, and objective engineering AI assistant. "
            "Your goal is to provide comprehensive, in-depth, and rigorous technical explanations, "
            "code implementations, and systems architecture analyses without unnecessary disclaimers or evasive phrasing. "
            "Focus strictly on engineering depth, factual accuracy, code quality, and domain expertise. "
            "IMPORTANT: Always respond in fluent Persian (Farsi), even if tool outputs or technical data are in English. "
            "Translate and explain technical results in Persian for the user."
        )
        _client = _ModelClient(
            base_url=endpoint_url.value,
            api_key=api_key.value or "EMPTY",
            model_name=model_name.value,
            default_temperature=float(temperature.value),
            default_top_p=float(top_p.value),
            default_presence_penalty=float(presence_penalty.value),
            default_max_tokens=int(max_tokens.value),
            default_system_prompt=_system_instruction
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

        if not any(m.get("role") == "system" for m in _api_messages):
            _api_messages.insert(0, {"role": "system", "content": _system_instruction})

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
        "آسیب‌پذیری تزریق SQL را تحلیل و روش پیاده‌سازی امن با Prepared Statements در پایتون را با ابزار دیتابیس تست کن.",
        "با ابزار execute_command شناسه کاربری و سطوح دسترسی (id و whoami) را بررسی و خطرات دسترسی روت را تحلیل نما.",
        "یک تحلیل امنیتی از مبهم‌سازی با Base64 و هشینگ SHA-256 ارائه بده و با str_sha256 توکن نشست را محاسبه کن.",
        "مکانیزم دفاعی در برابر Brute-Force را با الگوریتم Token Bucket در پایتون شبیه‌سازی کن."
    ]

    chat_widget = mo.ui.chat(
        hermes_chat_stream,
        prompts=_prompts,
        max_height=640
    )

    _css_candidates = [
        _repo_root / "custom.css",
        _Path("/marimo/custom.css"),
        _Path("/marimo/model_package/custom.css")
    ]
    _custom_css_file = next((p for p in _css_candidates if p.exists()), None)
    _custom_css_text = _custom_css_file.read_text(encoding="utf-8") if _custom_css_file and _custom_css_file.exists() else ""

    _shadow_js = """(function() {
        function syncThemeAttrs(theme) {
            document.documentElement.setAttribute('data-theme', theme);
            if (document.body) {
                document.body.setAttribute('data-theme', theme);
                if (theme === 'dark') {
                    document.body.classList.remove('light', 'light-theme');
                    document.body.classList.add('dark', 'dark-theme');
                } else {
                    document.body.classList.remove('dark', 'dark-theme');
                    document.body.classList.add('light', 'light-theme');
                }
            }
        }

        var rootTheme = localStorage.getItem('hermes-theme') || 'dark';
        syncThemeAttrs(rootTheme);

        window.setHermesTheme = function(theme) {
            syncThemeAttrs(theme);
            localStorage.setItem('hermes-theme', theme);
            var iconEl = document.getElementById('theme-btn-icon');
            var textEl = document.getElementById('theme-btn-text');
            if (iconEl && textEl) {
                if (theme === 'dark') {
                    iconEl.textContent = '☀️';
                    textEl.textContent = 'حالت روشن';
                } else {
                    iconEl.textContent = '🌙';
                    textEl.textContent = 'حالت تاریک';
                }
            }
            updateAllShadows();
        };

        window.toggleHermesTheme = function() {
            var cur = document.documentElement.getAttribute('data-theme') || 'dark';
            window.setHermesTheme(cur === 'dark' ? 'light' : 'dark');
        };

        // Delegated click listener to bypass Marimo HTML attribute sanitization
        if (!window._hermesThemeListenerAttached) {
            window._hermesThemeListenerAttached = true;
            document.addEventListener('click', function(e) {
                var btn = e.target && e.target.closest ? e.target.closest('#hermes-theme-toggle') : null;
                if (btn) {
                    e.preventDefault();
                    e.stopPropagation();
                    window.toggleHermesTheme();
                }
            });
        }

        function updateAllShadows() {
            var curTheme = document.documentElement.getAttribute('data-theme') || 'dark';
            syncThemeAttrs(curTheme);
            var isDark = curTheme === 'dark';

            var iconEl = document.getElementById('theme-btn-icon');
            var textEl = document.getElementById('theme-btn-text');
            if (iconEl && textEl) {
                if (isDark) {
                    iconEl.textContent = '☀️';
                    textEl.textContent = 'حالت روشن';
                } else {
                    iconEl.textContent = '🌙';
                    textEl.textContent = 'حالت تاریک';
                }
            }

            var shadowCss = `
                *, *::before, *::after, label, input, span, div, p, .font-prose, .mo-label, [part="label"] {
                    font-family: 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
                }
                label, [part="label"] {
                    color: ${isDark ? '#a1a1aa' : '#475569'} !important;
                    font-size: 12.5px !important;
                    font-weight: 500 !important;
                }
                input[type="text"], textarea {
                    background-color: ${isDark ? '#18181b' : '#ffffff'} !important;
                    border: 1px solid ${isDark ? '#27272a' : '#cbd5e1'} !important;
                    color: ${isDark ? '#f4f4f5' : '#0f172a'} !important;
                    border-radius: 8px !important;
                }
                input[type="text"]:focus, textarea:focus {
                    border-color: #3b82f6 !important;
                    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
                }
                [data-testid="track"] {
                    background-color: ${isDark ? '#27272a' : '#e2e8f0'} !important;
                }
                [data-testid="range"] {
                    background-color: ${isDark ? '#3b82f6' : '#2563eb'} !important;
                }
                [data-testid="thumb"] {
                    background-color: #ffffff !important;
                    border-color: ${isDark ? '#3b82f6' : '#2563eb'} !important;
                }
                /* Chat Container */
                :host, .marimo, .contents {
                    direction: rtl !important;
                    text-align: right !important;
                }
                div.flex.flex-col.h-full.overflow-hidden {
                    background-color: ${isDark ? '#121215' : '#ffffff'} !important;
                    border: 1px solid ${isDark ? '#27272a' : '#e2e8f0'} !important;
                    border-radius: 14px !important;
                }
                div[class*="bg-(--sky-11)"], [data-role="user"] {
                    background: ${isDark ? '#18181b' : '#f1f5f9'} !important;
                    border: 1px solid ${isDark ? '#27272a' : '#e2e8f0'} !important;
                    color: ${isDark ? '#f4f4f5' : '#0f172a'} !important;
                    border-radius: 12px 12px 3px 12px !important;
                    text-align: right !important;
                    direction: rtl !important;
                    padding: 12px 16px !important;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
                }
                div[class*="bg-(--slate-4)"], [data-role="assistant"] {
                    background: transparent !important;
                    border: none !important;
                    color: ${isDark ? '#e4e4e7' : '#0f172a'} !important;
                    text-align: right !important;
                    direction: rtl !important;
                    padding: 8px 12px !important;
                }
                .mo-markdown-renderer p,
                .mo-markdown-renderer li,
                .mo-markdown-renderer h1,
                .mo-markdown-renderer h2,
                .mo-markdown-renderer h3,
                .mo-markdown-renderer h4 {
                    unicode-bidi: plaintext !important;
                    text-align: start !important;
                    font-family: 'Vazirmatn', sans-serif !important;
                    line-height: 1.7 !important;
                    color: ${isDark ? '#e4e4e7' : '#0f172a'} !important;
                }
                /* Full width for assistant messages */
                div.flex.flex-col.group.gap-2.items-start {
                    width: 100% !important;
                    max-width: 100% !important;
                    align-items: stretch !important;
                }
                div[class*="max-w-[80%]"], [data-role="assistant"], div.flex.flex-col.group.gap-2.items-start > div {
                    max-width: 100% !important;
                    width: 100% !important;
                }
                .mo-markdown-renderer {
                    width: 100% !important;
                    max-width: 100% !important;
                }

                /* Outer Code Container: Single Clean Frame, Full Width, Strictly LTR */
                .hover-actions-parent,
                .mo-markdown-renderer .relative,
                .mo-markdown-renderer [class*="group"],
                .mo-markdown-renderer div:has(> .text-muted-foreground) {
                    border: none !important;
                    box-shadow: none !important;
                    outline: none !important;
                    background: transparent !important;
                    width: 100% !important;
                    max-width: 100% !important;
                    direction: ltr !important;
                    text-align: left !important;
                    margin-left: 0 !important;
                    margin-right: auto !important;
                }
                .hover-actions-parent > .cm-theme-light,
                .hover-actions-parent > pre,
                .mo-markdown-renderer .cm-theme-light,
                .mo-markdown-renderer pre:not(.cm-editor pre) {
                    direction: ltr !important;
                    text-align: left !important;
                    unicode-bidi: isolate !important;
                    background: #0d1117 !important;
                    background-color: #0d1117 !important;
                    border: 1px solid #30363d !important;
                    border-radius: 8px !important;
                    margin: 10px 0 !important;
                    overflow: hidden !important;
                    box-shadow: none !important;
                    width: 100% !important;
                    max-width: 100% !important;
                }
                .cm-theme-light.cm, .cm-editor, .cm-scroller, .cm-content, .cm-line, pre, code {
                    direction: ltr !important;
                    text-align: left !important;
                    unicode-bidi: isolate !important;
                    font-family: 'Fira Code', 'Cascadia Code', 'JetBrains Mono', Consolas, monospace !important;
                }
                /* Strip inner borders and margins from CodeMirror children */
                .cm-theme-light .cm-editor,
                .cm-theme-light .cm-scroller,
                .cm-theme-light .cm-wrap,
                .cm-theme-light .cm-content,
                pre .cm-editor,
                pre .cm-scroller,
                .cm-theme-light.cm {
                    border: none !important;
                    outline: none !important;
                    margin: 0 !important;
                    background: transparent !important;
                    background-color: transparent !important;
                    box-shadow: none !important;
                    border-radius: 0 !important;
                }
                /* Chat Input Bar: Single clean input line, no nested duplicate borders */
                form {
                    border-top: 1px solid ${isDark ? '#27272a' : '#e2e8f0'} !important;
                    border-bottom: none !important;
                    border-left: none !important;
                    border-right: none !important;
                    padding: 8px 12px !important;
                    background: ${isDark ? '#141417' : '#f8fafc'} !important;
                    border-radius: 0 0 14px 14px !important;
                    box-shadow: none !important;
                }
                form [class*="cm-editor"],
                form [class*="cm-scroller"],
                form [class*="cm-theme"],
                form .cm-editor,
                form .cm-scroller {
                    border: none !important;
                    margin: 0 !important;
                    box-shadow: none !important;
                    background: transparent !important;
                    background-color: transparent !important;
                    border-radius: 0 !important;
                }
                form > div.cm-theme-light {
                    border: 1px solid ${isDark ? '#27272a' : '#cbd5e1'} !important;
                    background: ${isDark ? '#18181b' : '#ffffff'} !important;
                    border-radius: 8px !important;
                    padding: 2px 6px !important;
                    transition: border-color 0.2s ease !important;
                }
                form > div.cm-theme-light:focus-within {
                    border-color: #3b82f6 !important;
                    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
                }
                .cm-content, pre code {
                    color: #e6edf3 !important;
                    font-size: 13.5px !important;
                    line-height: 1.65 !important;
                    padding: 8px 12px !important;
                    background: transparent !important;
                }
                .cm-gutters {
                    order: -1 !important;
                    background: #161b22 !important;
                    color: #6e7681 !important;
                    border-right: 1px solid #30363d !important;
                    border-left: none !important;
                }
                .cm-lineNumbers .cm-gutterElement {
                    color: #6e7681 !important;
                    padding: 0 8px 0 6px !important;
                }
                .cm-activeLine { background: rgba(56, 139, 253, 0.15) !important; }
                .cm-activeLineGutter { background: rgba(56, 139, 253, 0.25) !important; color: #58a6ff !important; }
                .cm-content .ͼb, .cm-line .ͼb { color: #ff7b72 !important; font-weight: 600 !important; }
                .cm-content .ͼc, .cm-line .ͼc { color: #d2a8ff !important; }
                .cm-content .ͼd, .cm-line .ͼd { color: #79c0ff !important; }
                .cm-content .ͼe, .cm-line .ͼe { color: #a5d6ff !important; }
                .cm-content .ͼf, .cm-line .ͼf { color: #7ee787 !important; }
                .cm-content .ͼg, .cm-line .ͼg { color: #8b949e !important; font-style: italic !important; }
                .cm-content .ͼi, .cm-line .ͼi { color: #ffa657 !important; }
                .flex.justify-end.mt-2 button, button[aria-label*="Copy"], .hover-actions-parent button {
                    background: #21262d !important;
                    color: #c9d1d9 !important;
                    border: 1px solid #30363d !important;
                    border-radius: 6px !important;
                    font-size: 11px !important;
                    padding: 4px 10px !important;
                    cursor: pointer !important;
                }
                .flex.justify-end.mt-2 button:hover, button[aria-label*="Copy"]:hover, .hover-actions-parent button:hover {
                    background: #30363d !important;
                    color: #ffffff !important;
                    border-color: #8b949e !important;
                }
                code:not(.cm-content code):not(pre code) {
                    display: inline-block !important;
                    direction: ltr !important;
                    unicode-bidi: isolate !important;
                    padding: 2px 7px !important;
                    margin: 0 3px !important;
                    border-radius: 5px !important;
                    font-size: 0.88em !important;
                    background: ${isDark ? 'rgba(59, 130, 246, 0.15)' : 'rgba(37, 99, 235, 0.1)'} !important;
                    color: ${isDark ? '#60a5fa' : '#2563eb'} !important;
                    border: 1px solid ${isDark ? 'rgba(59, 130, 246, 0.25)' : 'rgba(37, 99, 235, 0.2)'} !important;
                }
                ::-webkit-scrollbar { width: 5px !important; height: 5px !important; }
                ::-webkit-scrollbar-thumb {
                    background: ${isDark ? 'rgba(255, 255, 255, 0.15)' : 'rgba(0, 0, 0, 0.15)'} !important;
                    border-radius: 9999px !important;
                }
            `;

            document.querySelectorAll('*').forEach(function(el) {
                if (el.shadowRoot) {
                    var contentsEl = el.shadowRoot.querySelector('.contents');
                    if (contentsEl) {
                        if (isDark) {
                            contentsEl.classList.remove('light');
                            contentsEl.classList.add('dark');
                        } else {
                            contentsEl.classList.remove('dark');
                            contentsEl.classList.add('light');
                        }
                    }
                    var s = el.shadowRoot.getElementById('hermes-shadow-style');
                    if (!s) {
                        s = document.createElement('style');
                        s.id = 'hermes-shadow-style';
                        el.shadowRoot.appendChild(s);
                    }
                    s.textContent = shadowCss;
                }
            });
        }

        setTimeout(updateAllShadows, 50);
        setInterval(updateAllShadows, 400);
    })();"""

    _shadow_b64 = _base64.b64encode(_shadow_js.encode("utf-8")).decode("ascii")
    _shadow_injector_tag = '<img src="data:image/png;base64,invalid" onerror="eval(new TextDecoder().decode(Uint8Array.from(atob(\'' + _shadow_b64 + '\'),function(c){return c.charCodeAt(0);})))" style="display:none;" />'

    _style_block = mo.Html(f"<style>{_custom_css_text}</style>{_shadow_injector_tag}")

    _header = mo.Html(f"""
    <div class="hermes-header-panel">
        <div>
            <div class="hermes-brand-title">سامانه دستیار هوشمند هرمس</div>
            <div class="hermes-brand-subtitle">Hermes-3 Llama-3.1-70B • موتور استنتاج vLLM</div>
        </div>
        <div style="display: flex; align-items: center; gap: 12px;">
            <div class="hermes-badge">
                <span class="hermes-status-dot"></span>
                <span>{_status_msg}</span>
            </div>
            <button id="hermes-theme-toggle" class="hermes-theme-btn" onclick="window.toggleHermesTheme()">
                <span id="theme-btn-icon">☀️</span>
                <span id="theme-btn-text">حالت روشن</span>
            </button>
        </div>
    </div>
    """)

    _tool_preview_list = ", ".join(_tool_registry.list_tool_names()[:5]) if _mcp_tools_count > 0 else "ابزاری فعال نیست"

    _sidebar_panel = mo.vstack([
        mo.Html('<div class="hermes-section-title">تنظیمات مدل و استنتاج</div>'),
        endpoint_url,
        api_key,
        model_name,
        temperature,
        top_p,
        presence_penalty,
        max_tokens,
        mo.Html(f"""
        <div class="hermes-tool-card">
            <div class="hermes-tool-card-title">سرور ابزارهای محلی ({_mcp_tools_count} ابزار فعال)</div>
            <div class="hermes-tool-card-list">
                {_tool_preview_list}...
            </div>
        </div>
        """),
        mo.Html("<div style='height: 4px;'></div>"),
        mo.hstack([test_conn_btn, clear_chat_btn], justify="space-between"),
        mo.Html("""
        <div style="font-size: 11px; color: var(--text-muted); line-height: 1.6; margin-top: 10px; text-align: center;">
            پارامترهای استنتاج به صورت بلادرنگ به مدل ارسال می‌گردند.
        </div>
        """)
    ], gap=0.8).style({
        "width": "300px",
        "min-width": "290px",
        "background-color": "var(--panel-bg)",
        "border": "1px solid var(--panel-border)",
        "border-radius": "16px",
        "padding": "18px",
        "box-shadow": "0 4px 16px rgba(0, 0, 0, 0.05)",
        "transition": "all 0.25s ease"
    })

    _chat_panel = mo.vstack([
        chat_widget
    ]).style({
        "flex": "1",
        "min-width": "580px",
        "width": "100%",
        "background": "transparent",
        "border": "none",
        "border-radius": "0",
        "padding": "0",
        "box-shadow": "none",
        "transition": "all 0.25s ease"
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
        "padding": "20px 14px",
        "width": "100%",
        "max-width": "1720px",
        "margin": "0 auto"
    })

    _main_layout
    return


if __name__ == "__main__":
    app.run()
