import re
from pathlib import Path

repo_dir = Path(r"C:\Users\farha\.gemini\antigravity\scratch\Hermes-Black-bird")
nb_file = repo_dir / "notebook.py"
nb_text = nb_file.read_text(encoding="utf-8")

# 1. Update shadowCss in notebook.py
old_shadow_code_pattern = r"/\* Full width for assistant messages \*/[\s\S]*?(?=/\* Chat Input Bar: Reset nested CodeMirror borders \*/)"

new_shadow_code = """/* Full width for assistant messages */
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
                """

nb_text = re.sub(old_shadow_code_pattern, new_shadow_code, nb_text)

# 2. Update form styles in shadowCss
old_form_pattern = r"/\* Chat Input Bar: Reset nested CodeMirror borders \*/[\s\S]*?(?=\.cm-content, pre code \{)"
new_form_code = """/* Chat Input Bar: Single clean input line, no nested duplicate borders */
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
                """
nb_text = re.sub(old_form_pattern, new_form_code, nb_text)

# 3. Update _sidebar_panel, _chat_panel, _main_layout styles
old_panels_pattern = r'_sidebar_panel = mo\.vstack\(\[[\s\S]*?\)\.style\(\{[\s\S]*?\}\)\s*_chat_panel = mo\.vstack\(\[[\s\S]*?\)\.style\(\{[\s\S]*?\}\)\s*_main_layout = mo\.vstack\(\[[\s\S]*?\)\.style\(\{[\s\S]*?\}\)'

new_panels_code = """_sidebar_panel = mo.vstack([
        mo.Html('<div class="hermes-section-title">تنظیمات مدل و استنتاج</div>'),
        endpoint_url,
        api_key,
        model_name,
        temperature,
        top_p,
        presence_penalty,
        max_tokens,
        mo.Html(f\"\"\"
        <div class="hermes-tool-card">
            <div class="hermes-tool-card-title">سرور ابزارهای محلی ({_mcp_tools_count} ابزار فعال)</div>
            <div class="hermes-tool-card-list">
                {_tool_preview_list}...
            </div>
        </div>
        \"\"\"),
        mo.Html("<div style='height: 4px;'></div>"),
        mo.hstack([test_conn_btn, clear_chat_btn], justify="space-between"),
        mo.Html(\"\"\"
        <div style="font-size: 11px; color: var(--text-muted); line-height: 1.6; margin-top: 10px; text-align: center;">
            پارامترهای استنتاج به صورت بلادرنگ به مدل ارسال می‌گردند.
        </div>
        \"\"\")
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
    })"""

nb_text = re.sub(old_panels_pattern, new_panels_code, nb_text)

nb_file.write_text(nb_text, encoding="utf-8")
print("Updated notebook.py successfully.")
