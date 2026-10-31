import re
from pathlib import Path

repo_dir = Path(r"C:\Users\farha\.gemini\antigravity\scratch\Hermes-Black-bird")
css_file = repo_dir / "custom.css"
nb_file = repo_dir / "notebook.py"

# 1. Update custom.css
css_text = css_file.read_text(encoding="utf-8")

# Add fluid wide layout if not present
if "Wide-Screen Fluid Layout" not in css_text:
    css_text = css_text.replace(
        """.marimo-app {
  background-color: var(--app-bg) !important;
  color: var(--text-primary) !important;
  direction: rtl !important;
  text-align: right !important;
}""",
        """.marimo-app {
  background-color: var(--app-bg) !important;
  color: var(--text-primary) !important;
  direction: rtl !important;
  text-align: right !important;
}

/* --------------------------------------------------------------------------
   Wide-Screen Fluid Layout (Expand Marimo page & outputs)
   -------------------------------------------------------------------------- */

:root {
  --content-width-medium: 100% !important;
  --content-width-large: 100% !important;
}

[class*="max-w-(--content-width-medium)"],
.max-w-\\(--content-width-medium\\),
.marimo-cell,
.output-area,
.output {
  max-width: 100% !important;
  width: 100% !important;
}

div.m-auto {
  max-width: 100% !important;
}

/* Optimize excessive horizontal padding on large screens */
div[class*="xl:px-24"],
div[class*="md:px-20"],
div[class*="sm:px-16"] {
  padding-left: 20px !important;
  padding-right: 20px !important;
}"""
    )

# Replace code styling block in custom.css
old_code_block_pattern = r"/\* Outer Code Container: ONLY ONE BORDER & strictly Left-Aligned \(LTR\) \*/[\s\S]*?(?=/\* Syntax Highlighting \*/)"
new_code_block = """/* Outer Code Container: Single Clean Frame, Full Width, Strictly LTR */
div.flex.flex-col.group.gap-2.items-start {
  width: 100% !important;
  max-width: 100% !important;
  align-items: stretch !important;
}

div[class*="max-w-[80%]"],
[data-role="assistant"],
div.flex.flex-col.group.gap-2.items-start > div {
  max-width: 100% !important;
  width: 100% !important;
}

.mo-markdown-renderer {
  width: 100% !important;
  max-width: 100% !important;
}

/* Strip redundant borders and wrappers around code blocks */
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

/* ONLY ONE clean border on the CodeMirror container */
.hover-actions-parent > .cm-theme-light,
.hover-actions-parent > pre,
.mo-markdown-renderer .cm-theme-light,
.mo-markdown-renderer pre:not(.cm-editor pre) {
  direction: ltr !important;
  text-align: left !important;
  unicode-bidi: isolate !important;
  background-color: var(--code-bg) !important;
  background: var(--code-bg) !important;
  border: 1px solid var(--code-border) !important;
  border-radius: 8px !important;
  box-shadow: none !important;
  margin: 10px 0 !important;
  overflow: hidden !important;
  width: 100% !important;
  max-width: 100% !important;
}

/* Strip inner borders, backgrounds, and margins from CodeMirror children */
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
  direction: ltr !important;
  text-align: left !important;
  unicode-bidi: isolate !important;
}

/* Chat Input Bar: Reset nested CodeMirror borders so only ONE clean bar exists */
form {
  border-top: 1px solid var(--panel-border) !important;
  border-bottom: none !important;
  border-left: none !important;
  border-right: none !important;
  padding: 8px 12px !important;
  background: var(--panel-surface) !important;
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
  border: 1px solid var(--panel-border) !important;
  background: var(--input-bg) !important;
  border-radius: 8px !important;
  padding: 2px 6px !important;
  transition: border-color 0.2s ease !important;
}

form > div.cm-theme-light:focus-within {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 2px var(--accent-muted) !important;
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
  unicode-bidi: isolate !important;
}

.cm-gutters {
  order: -1 !important;
  direction: ltr !important;
  background-color: var(--code-gutter-bg) !important;
  background: var(--code-gutter-bg) !important;
  color: var(--code-gutter-text) !important;
  border-right: 1px solid var(--code-gutter-border) !important;
  border-left: none !important;
  border-top: none !important;
  border-bottom: none !important;
}

.cm-lineNumbers .cm-gutterElement {
  color: var(--code-gutter-text) !important;
  padding: 0 8px 0 6px !important;
}

"""

css_text = re.sub(old_code_block_pattern, new_code_block, css_text)
css_file.write_text(css_text, encoding="utf-8")
print("Updated custom.css successfully.")
