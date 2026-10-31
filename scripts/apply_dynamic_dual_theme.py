import re
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent

# 1. Update custom.css
custom_css_file = repo_root / "custom.css"
old_css = custom_css_file.read_text(encoding="utf-8")

# Extract the offline font definitions (lines 1 to 16)
font_lines = []
for line in old_css.splitlines():
    font_lines.append(line)
    if line.strip() == "}":
        # Check if we got both Vazirmatn @font-face blocks
        if len("\n".join(font_lines)) > 100000:
            break

fonts_block = "\n".join(font_lines[:16])

new_css_body = """
/* --------------------------------------------------------------------------
   Dynamic Dual-Theme Design Tokens (Linear & Vercel Inspired)
   -------------------------------------------------------------------------- */

:root, [data-theme="dark"] {
  --app-bg: #09090b;
  --panel-bg: #121215;
  --panel-surface: #18181b;
  --panel-border: #27272a;
  --panel-border-subtle: rgba(255, 255, 255, 0.08);
  --panel-hover: #222226;
  --text-primary: #f4f4f5;
  --text-secondary: #a1a1aa;
  --text-muted: #71717a;
  --accent: #3b82f6;
  --accent-hover: #2563eb;
  --accent-muted: rgba(59, 130, 246, 0.15);
  --code-bg: #0d1117;
  --code-gutter-bg: #161b22;
  --code-border: #30363d;
  --code-text: #e6edf3;
  --user-msg-bg: #18181b;
  --user-msg-border: #27272a;
  --user-msg-text: #f4f4f5;
  --asst-msg-text: #e4e4e7;
  --badge-bg: rgba(16, 185, 129, 0.12);
  --badge-border: rgba(16, 185, 129, 0.28);
  --badge-text: #34d399;
  --status-dot: #10b981;
  --scrollbar-thumb: rgba(255, 255, 255, 0.15);
  --scrollbar-thumb-hover: rgba(255, 255, 255, 0.28);
  --input-bg: #18181b;
  --input-border: #27272a;
  --input-text: #f4f4f5;
  --slider-track: #27272a;
  --slider-range: #3b82f6;
  --slider-thumb: #ffffff;
}

[data-theme="light"] {
  --app-bg: #f8fafc;
  --panel-bg: #ffffff;
  --panel-surface: #f8fafc;
  --panel-border: #e2e8f0;
  --panel-border-subtle: #edf2f7;
  --panel-hover: #f1f5f9;
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --text-muted: #64748b;
  --accent: #2563eb;
  --accent-hover: #1d4ed8;
  --accent-muted: rgba(37, 99, 235, 0.08);
  --code-bg: #0f172a;
  --code-gutter-bg: #1e293b;
  --code-border: #334155;
  --code-text: #f8fafc;
  --user-msg-bg: #f1f5f9;
  --user-msg-border: #e2e8f0;
  --user-msg-text: #0f172a;
  --asst-msg-text: #0f172a;
  --badge-bg: rgba(16, 185, 129, 0.1);
  --badge-border: rgba(16, 185, 129, 0.25);
  --badge-text: #059669;
  --status-dot: #10b981;
  --scrollbar-thumb: rgba(0, 0, 0, 0.15);
  --scrollbar-thumb-hover: rgba(0, 0, 0, 0.28);
  --input-bg: #ffffff;
  --input-border: #cbd5e1;
  --input-text: #0f172a;
  --slider-track: #e2e8f0;
  --slider-range: #2563eb;
  --slider-thumb: #ffffff;
}

/* --------------------------------------------------------------------------
   Global Typography & Layout
   -------------------------------------------------------------------------- */

*, *::before, *::after,
html, body, .marimo, .marimo-app,
h1, h2, h3, h4, h5, h6,
p, span, div, a, li, ol, ul,
label, button, input, textarea, select,
.marimo-ui-element {
  font-family: 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
  box-sizing: border-box;
}

code, pre, pre code, kbd, samp, var,
.cm-editor, .cm-scroller, .cm-content,
.cm-gutter, .cm-lineNumbers, .font-mono {
  font-family: 'Fira Code', 'Cascadia Code', 'JetBrains Mono', Consolas, monospace !important;
}

html, body {
  background-color: var(--app-bg) !important;
  color: var(--text-primary) !important;
  direction: rtl !important;
  text-align: right !important;
  margin: 0;
  padding: 0;
  transition: background-color 0.25s ease, color 0.25s ease;
}

.marimo-app {
  background-color: var(--app-bg) !important;
  color: var(--text-primary) !important;
  direction: rtl !important;
  text-align: right !important;
}

/* --------------------------------------------------------------------------
   Hermes Unified Application Panels (Adaptive Design)
   -------------------------------------------------------------------------- */

.hermes-app-container {
  background-color: var(--app-bg) !important;
  border: 1px solid var(--panel-border) !important;
  border-radius: 20px !important;
  padding: 24px !important;
  direction: rtl !important;
  text-align: right !important;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15) !important;
  transition: all 0.25s ease !important;
}

.hermes-header-panel {
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  padding: 16px 22px !important;
  background-color: var(--panel-bg) !important;
  border: 1px solid var(--panel-border) !important;
  border-radius: 14px !important;
  margin-bottom: 20px !important;
  transition: all 0.25s ease !important;
}

.hermes-sidebar-panel {
  background-color: var(--panel-bg) !important;
  border: 1px solid var(--panel-border) !important;
  border-radius: 16px !important;
  padding: 20px !important;
  width: 330px !important;
  min-width: 310px !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05) !important;
  transition: all 0.25s ease !important;
}

.hermes-chat-panel {
  background-color: var(--panel-bg) !important;
  border: 1px solid var(--panel-border) !important;
  border-radius: 16px !important;
  padding: 16px !important;
  flex: 1 !important;
  min-width: 460px !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05) !important;
  transition: all 0.25s ease !important;
}

/* --------------------------------------------------------------------------
   Header Components & Theme Switcher
   -------------------------------------------------------------------------- */

.hermes-brand-title {
  font-size: 16px !important;
  font-weight: 700 !important;
  color: var(--text-primary) !important;
  letter-spacing: -0.2px !important;
  margin-bottom: 3px !important;
}

.hermes-brand-subtitle {
  font-size: 12px !important;
  font-weight: 500 !important;
  color: var(--text-muted) !important;
  letter-spacing: -0.1px !important;
}

.hermes-badge {
  display: inline-flex !important;
  align-items: center !important;
  gap: 8px !important;
  padding: 5px 12px !important;
  border-radius: 9999px !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  background-color: var(--badge-bg) !important;
  border: 1px solid var(--badge-border) !important;
  color: var(--badge-text) !important;
}

.hermes-status-dot {
  width: 7px !important;
  height: 7px !important;
  border-radius: 50% !important;
  background-color: var(--status-dot) !important;
  display: inline-block !important;
}

.hermes-theme-btn {
  display: inline-flex !important;
  align-items: center !important;
  gap: 8px !important;
  padding: 6px 14px !important;
  border-radius: 8px !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  cursor: pointer !important;
  background-color: var(--panel-surface) !important;
  color: var(--text-primary) !important;
  border: 1px solid var(--panel-border) !important;
  transition: all 0.2s ease !important;
}

.hermes-theme-btn:hover {
  background-color: var(--panel-hover) !important;
  border-color: var(--accent) !important;
}

/* --------------------------------------------------------------------------
   Sidebar Components
   -------------------------------------------------------------------------- */

.hermes-section-title {
  font-size: 13.5px !important;
  font-weight: 700 !important;
  color: var(--text-primary) !important;
  padding-bottom: 8px !important;
  margin-bottom: 12px !important;
  border-bottom: 1px solid var(--panel-border) !important;
}

.hermes-tool-card {
  background-color: var(--panel-surface) !important;
  border: 1px solid var(--panel-border) !important;
  border-radius: 10px !important;
  padding: 12px 14px !important;
  margin: 10px 0 !important;
}

.hermes-tool-card-title {
  font-size: 12.5px !important;
  font-weight: 600 !important;
  color: var(--text-primary) !important;
  margin-bottom: 4px !important;
}

.hermes-tool-card-list {
  font-size: 11px !important;
  font-family: 'Fira Code', monospace !important;
  direction: ltr !important;
  text-align: left !important;
  color: var(--accent) !important;
  background-color: var(--app-bg) !important;
  padding: 5px 8px !important;
  border-radius: 6px !important;
  border: 1px solid var(--panel-border) !important;
}

/* --------------------------------------------------------------------------
   CodeMirror & LTR Rules (Dark Terminal in both themes)
   -------------------------------------------------------------------------- */

.cm-theme-light.cm,
.cm-editor,
.cm-scroller,
.cm-theme-light .cm-editor,
pre {
  direction: ltr !important;
  text-align: left !important;
  unicode-bidi: isolate !important;
  background-color: var(--code-bg) !important;
  background: var(--code-bg) !important;
  border: 1px solid var(--code-border) !important;
  border-radius: 10px !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
  margin: 12px 0 !important;
  overflow: hidden !important;
}

.cm-content, pre code {
  color: var(--code-text) !important;
  font-size: 13.5px !important;
  line-height: 1.65 !important;
  padding: 8px 12px !important;
  background: transparent !important;
  background-color: transparent !important;
}

.cm-line {
  color: var(--code-text) !important;
  direction: ltr !important;
  text-align: left !important;
}

.cm-gutters {
  order: -1 !important;
  background-color: var(--code-gutter-bg) !important;
  background: var(--code-gutter-bg) !important;
  color: var(--code-gutter-text) !important;
  border-right: 1px solid var(--code-gutter-border) !important;
  border-left: none !important;
}

.cm-lineNumbers .cm-gutterElement {
  color: var(--code-gutter-text) !important;
  padding: 0 8px 0 6px !important;
}

/* Syntax Highlighting */
.cm-content .ͼb, .cm-line .ͼb { color: #ff7b72 !important; font-weight: 600 !important; }
.cm-content .ͼc, .cm-line .ͼc { color: #d2a8ff !important; }
.cm-content .ͼd, .cm-line .ͼd { color: #79c0ff !important; }
.cm-content .ͼe, .cm-line .ͼe { color: #a5d6ff !important; }
.cm-content .ͼf, .cm-line .ͼf { color: #7ee787 !important; }
.cm-content .ͼg, .cm-line .ͼg { color: #8b949e !important; font-style: italic !important; }
.cm-content .ͼi, .cm-line .ͼi { color: #ffa657 !important; }

/* Inline Code */
code:not(.cm-content code):not(pre code) {
  display: inline-block !important;
  direction: ltr !important;
  unicode-bidi: isolate !important;
  padding: 2px 7px !important;
  margin: 0 3px !important;
  border-radius: 5px !important;
  font-size: 0.88em !important;
  background-color: var(--accent-muted) !important;
  color: var(--accent) !important;
  border: 1px solid var(--panel-border) !important;
}

/* Copy Buttons */
.flex.justify-end.mt-2 button,
button[aria-label*="Copy"],
.hover-actions-parent button {
  background-color: #21262d !important;
  color: #c9d1d9 !important;
  border: 1px solid #30363d !important;
  border-radius: 6px !important;
  font-size: 11px !important;
  padding: 4px 10px !important;
  font-weight: 500 !important;
  cursor: pointer !important;
  transition: all 0.2s ease !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 4px !important;
}

.flex.justify-end.mt-2 button:hover,
button[aria-label*="Copy"]:hover,
.hover-actions-parent button:hover {
  background-color: #30363d !important;
  color: #ffffff !important;
  border-color: #8b949e !important;
}

/* --------------------------------------------------------------------------
   Minimalist Scrollbar
   -------------------------------------------------------------------------- */

::-webkit-scrollbar, *::-webkit-scrollbar {
  width: 5px !important;
  height: 5px !important;
}
::-webkit-scrollbar-track, *::-webkit-scrollbar-track {
  background: transparent !important;
}
::-webkit-scrollbar-thumb, *::-webkit-scrollbar-thumb {
  background: var(--scrollbar-thumb) !important;
  border-radius: 9999px !important;
}
::-webkit-scrollbar-thumb:hover, *::-webkit-scrollbar-thumb:hover {
  background: var(--scrollbar-thumb-hover) !important;
}
"""

final_css = fonts_block + "\n" + new_css_body
custom_css_file.write_text(final_css, encoding="utf-8")
print("[+] Updated custom.css successfully.")
