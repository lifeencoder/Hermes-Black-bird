import os

new_styles = """
/* ==========================================================================
   HERMES BLACK BIRD - MODERN GLASSMORPHYSIM RTL & CODE STYLING
   ========================================================================== */

/* 1. Global Font: Vazirmatn for all UI elements */
*, *::before, *::after,
html, body, .marimo, .marimo-app,
h1, h2, h3, h4, h5, h6,
p, span, div, a, li, ol, ul,
label, button, input, textarea, select,
.marimo-ui-element, .glass-app-container,
.glass-header-panel, .glass-sidebar-panel, .glass-chat-panel {
  font-family: 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
}

/* Monospace fonts exclusively for code */
code, pre, pre code, kbd, samp, var,
.cm-editor, .cm-scroller, .cm-content,
.cm-gutter, .cm-lineNumbers, .font-mono {
  font-family: 'Fira Code', 'Cascadia Code', 'JetBrains Mono', Consolas, 'Courier New', monospace !important;
}

/* 2. Global Direction & RTL Alignment */
html, body, .marimo-app, .glass-app-container, marimo-chatbot {
  direction: rtl !important;
  text-align: right !important;
}

/* Markdown Bidirectional Support: English/Code LTR, Persian RTL */
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
}

/* 3. CODE BLOCKS: Strictly LTR & Left-Aligned */
pre, code,
.cm-theme-light.cm,
.cm-editor,
.cm-scroller,
.cm-content,
.cm-line,
.hover-actions-parent,
.mo-markdown-renderer pre,
.mo-markdown-renderer code {
  direction: ltr !important;
  text-align: left !important;
  unicode-bidi: isolate !important;
}

/* Inline Code Elements */
code:not(.cm-content code):not(pre code) {
  display: inline-block !important;
  direction: ltr !important;
  unicode-bidi: isolate !important;
  padding: 2px 7px !important;
  margin: 0 3px !important;
  border-radius: 6px !important;
  font-size: 0.88em !important;
  background: rgba(2, 132, 199, 0.1) !important;
  color: #0284c7 !important;
  border: 1px solid rgba(2, 132, 199, 0.25) !important;
}

/* 4. Code Blocks: Modern Sleek Dark Theme */
.cm-theme-light.cm,
pre {
  background: #0f172a !important; /* Deep Slate 900 */
  border: 1px solid #334155 !important;
  border-radius: 12px !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.18), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
  margin: 12px 0 !important;
  overflow: hidden !important;
}

.cm-content, pre code {
  color: #f1f5f9 !important; /* Slate 100 */
  font-size: 13.5px !important;
  line-height: 1.65 !important;
  padding: 8px 12px !important;
  background: transparent !important;
}

.cm-gutters {
  background: #1e293b !important; /* Slate 800 */
  color: #64748b !important;
  border-right: 1px solid #334155 !important;
  border-left: none !important;
  order: -1 !important;
}

.cm-lineNumbers .cm-gutterElement {
  color: #64748b !important;
  padding: 0 8px 0 6px !important;
}

.cm-activeLine {
  background: rgba(51, 65, 85, 0.45) !important;
}

.cm-activeLineGutter {
  background: rgba(51, 65, 85, 0.7) !important;
  color: #38bdf8 !important;
}

/* 5. Copy Buttons & Action Bars */
.flex.justify-end.mt-2 button,
button[aria-label*="Copy"],
.hover-actions-parent button {
  background: #1e293b !important;
  color: #e2e8f0 !important;
  border: 1px solid #475569 !important;
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
  background: #0284c7 !important;
  color: #ffffff !important;
  border-color: #0284c7 !important;
  box-shadow: 0 2px 8px rgba(2, 132, 199, 0.3) !important;
}

/* 6. Chat Bubbles */
marimo-chatbot [data-role="user"],
marimo-chatbot .user-message,
div.max-w-\\[80\\%\\].bg-\\(--sky-11\\) {
  background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
  color: #ffffff !important;
  border-radius: 16px 16px 4px 16px !important;
  box-shadow: 0 4px 14px rgba(2, 132, 199, 0.2) !important;
  text-align: right !important;
  direction: rtl !important;
  padding: 12px 16px !important;
}

marimo-chatbot [data-role="assistant"],
marimo-chatbot .assistant-message,
div.max-w-\\[80\\%\\].bg-\\(--slate-4\\) {
  background: rgba(255, 255, 255, 0.95) !important;
  border: 1px solid rgba(226, 232, 240, 0.9) !important;
  color: #0f172a !important;
  border-radius: 16px 16px 16px 4px !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04) !important;
  text-align: right !important;
  direction: rtl !important;
  padding: 12px 16px !important;
}

marimo-chatbot textarea, marimo-chatbot input {
  direction: rtl !important;
  text-align: right !important;
  font-family: 'Vazirmatn', sans-serif !important;
  background: rgba(255, 255, 255, 0.95) !important;
  border: 1px solid #cbd5e1 !important;
  color: #0f172a !important;
  border-radius: 12px !important;
}

marimo-chatbot textarea:focus, marimo-chatbot input:focus {
  border-color: #0284c7 !important;
  box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15) !important;
}

/* 7. Custom Minimalist Glassmorphic Scrollbar */
::-webkit-scrollbar,
*::-webkit-scrollbar {
  width: 6px !important;
  height: 6px !important;
}

::-webkit-scrollbar-track,
*::-webkit-scrollbar-track {
  background: transparent !important;
}

::-webkit-scrollbar-thumb,
*::-webkit-scrollbar-thumb {
  background: rgba(148, 163, 184, 0.45) !important;
  border-radius: 9999px !important;
}

::-webkit-scrollbar-thumb:hover,
*::-webkit-scrollbar-thumb:hover {
  background: rgba(100, 116, 139, 0.75) !important;
}

/* 8. Typing Indicator Animation */
@keyframes typing-pulse {
  0%, 80%, 100% {
    transform: scale(0.6);
    opacity: 0.3;
  }
  40% {
    transform: scale(1.1);
    opacity: 1;
  }
}

.typing-indicator {
  display: inline-flex !important;
  align-items: center !important;
  gap: 5px !important;
  padding: 8px 14px !important;
  border-radius: 12px !important;
  background: rgba(241, 245, 249, 0.8) !important;
}

.typing-dot {
  width: 7px !important;
  height: 7px !important;
  border-radius: 50% !important;
  background: #0284c7 !important;
  animation: typing-pulse 1.4s infinite ease-in-out both !important;
}

.typing-dot:nth-child(1) { animation-delay: -0.32s !important; }
.typing-dot:nth-child(2) { animation-delay: -0.16s !important; }
.typing-dot:nth-child(3) { animation-delay: 0s !important; }

/* 9. Pulsing Status Dots */
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
  width: 10px !important;
  height: 10px !important;
  background-color: #10b981 !important;
  border-radius: 50% !important;
  display: inline-block !important;
  animation: pulse-green-glow 2s infinite !important;
}

.dot-red {
  width: 10px !important;
  height: 10px !important;
  background-color: #ef4444 !important;
  border-radius: 50% !important;
  display: inline-block !important;
  animation: pulse-red-glow 2s infinite !important;
}
"""

with open('custom.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

font_lines = lines[:16]

with open('custom.css', 'w', encoding='utf-8') as f:
    f.writelines(font_lines)
    f.write(new_styles)

print("custom.css updated successfully!")
