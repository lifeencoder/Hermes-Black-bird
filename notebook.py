# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "gdrive-fsspec==0.4.1",
#     "requests==2.34.2",
# ]
# ///

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell(hide_code=True)
def env_check():
    import sys, subprocess, os, json, shutil
    import marimo as mo


    return (mo,)


@app.cell(hide_code=True)
def gdrive_connect():
    from gdrive_fsspec import GoogleDriveFileSystem

    fs = GoogleDriveFileSystem(token="cache")

    return


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
        step=0.1,
        value=0.7,
        label="🌡️ دمای تولید (Temperature):",
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
        temperature,
        test_conn_btn,
    )


@app.cell(hide_code=True)
def persian_chat_app(
    api_key,
    clear_chat_btn,
    endpoint_url,
    max_tokens,
    mo,
    model_name,
    temperature,
    test_conn_btn,
):
    import requests as _requests
    from openai import OpenAI as _OpenAI

    # وابستگی به دکمه‌های کنترل
    _ = clear_chat_btn.value
    _ = test_conn_btn.value

    with open("/marimo/custom.css", "r", encoding="utf-8") as _f:
        _custom_css = _f.read()

    _style_block = mo.Html(f"<style>{_custom_css}</style>")

    _is_connected = False
    _status_msg = "در حال بررسی وضعیت..."
    try:
        _res = _requests.get(f"{endpoint_url.value.rstrip('/')}/models", timeout=3)
        if _res.status_code == 200:
            _models = _res.json().get("data", [])
            _m_ids = [m["id"] for m in _models]
            if model_name.value in _m_ids:
                _is_connected = True
                _status_msg = "متصل به سرور vLLM (پورت ۸۰۰۰)"
            else:
                _is_connected = True
                _status_msg = f"سرور متصل است ({len(_models)} مدل فعال)"
        else:
            _status_msg = f"خطای سرور: کد {_res.status_code}"
    except Exception as _e:
        _status_msg = "عدم برقراری ارتباط با سرور"

    def _hermes_chat_stream(messages, config):
        _client = _OpenAI(
            base_url=endpoint_url.value,
            api_key=api_key.value or "EMPTY"
        )
        _api_messages = [
            {
                "role": "system",
                "content": "تو یک دستیار هوش مصنوعی فارسی‌زبان هستی. پاسخ‌هایت بسیار دقیق، مفید، مستدل و به زبان فارسی شیوا و رسا باشد."
            }
        ]
        for _msg in messages:
            _role = getattr(_msg, "role", "user")
            _content = getattr(_msg, "content", "")
            if _content:
                _api_messages.append({"role": _role, "content": str(_content)})

        try:
            _stream = _client.chat.completions.create(
                model=model_name.value,
                messages=_api_messages,
                temperature=temperature.value,
                max_tokens=max_tokens.value,
                stream=True
            )
            for _chunk in _stream:
                if _chunk.choices and _chunk.choices[0].delta.content:
                    yield _chunk.choices[0].delta.content
        except Exception as _err:
            yield f"⚠️ **خطا در ارتباط با مدل:**\n\n`{str(_err)}`\n\nلطفاً از فعال بودن سرور و درستی آدرس Endpoint در نوار کناری مطمئن شوید."

    _prompts = [
        "یک تابع پایتون برای الگوریتم مرتب‌سازی سریع (QuickSort) بنویس.",
        "قانون اول نیوتن را با یک مثال روزمره و ملموس توضیح بده.",
        "تفاوت مدل‌های هوش مصنوعی زاینده (Generative AI) و سنتی چیست؟",
        "۳ راهکار کلیدی برای بهینه‌سازی دیتابیس در ترافیک بالا پیشنهاد بده."
    ]

    _chat_widget = mo.ui.chat(
        _hermes_chat_stream,
        prompts=_prompts,
        max_height=580
    )

    _header = mo.Html(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 14px 20px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; margin-bottom: 14px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04); font-family: 'Vazirmatn', sans-serif;">
        <div style="font-size: 19px; font-weight: 800; color: #0f172a; display: flex; align-items: center; gap: 8px;">
            <span style="color: #0284c7; font-size: 22px;">✨</span>
            <span>دستیار هوشمند Hermes-3 (Llama-3.1-70B FP8)</span>
        </div>
        <div style="display: inline-flex; align-items: center; gap: 8px; padding: 6px 14px; border-radius: 9999px; font-size: 13px; font-weight: 600; background: {'#ecfdf5' if _is_connected else '#fef2f2'}; border: 1px solid {'#a7f3d0' if _is_connected else '#fecaca'};">
            <span class="{'status-dot-green' if _is_connected else 'status-dot-red'}"></span>
            <span style="color: {'#065f46' if _is_connected else '#991b1b'};">{_status_msg}</span>
        </div>
    </div>
    """)

    _sidebar_panel = mo.vstack([
        mo.Html('<div style="font-size: 15px; font-weight: 700; color: #0f172a; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; margin-bottom: 12px; display: flex; align-items: center; gap: 6px; font-family: \'Vazirmatn\', sans-serif;">⚙️ تنظیمات مدل و اتصال</div>'),
        endpoint_url,
        api_key,
        model_name,
        temperature,
        max_tokens,
        mo.Html("<hr style='border-color: #e2e8f0; margin: 8px 0;'/>"),
        mo.hstack([test_conn_btn, clear_chat_btn], justify="space-between"),
        mo.Html("""
        <div style="font-size: 12px; color: #475569; line-height: 1.6; margin-top: 10px; background: #f8fafc; padding: 8px 12px; border-radius: 8px; border: 1px solid #e2e8f0; font-family: 'Vazirmatn', sans-serif;">
            💡 <b>راهنما:</b> تغییر دما و توکن‌ها بلادرنگ روی پاسخ‌های بعدی مدل اثر می‌گذارد.
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
        _chat_widget
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

    persian_chat_app_view

    return


if __name__ == "__main__":
    app.run()
