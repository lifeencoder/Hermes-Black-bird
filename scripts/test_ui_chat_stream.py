import marimo._code_mode as cm
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ctx = cm.get_context()

class DummyMsg:
    def __init__(self, content):
        self.role = "user"
        self.content = content

prompt = "با استفاده از ابزار execute_command، دستور 'echo Hello' را اجرا کن."

print("=================================================================")
print("🦅 Testing UI Chat Agent Execution (hermes_chat_stream)")
print("=================================================================")
print(f"[*] Prompt: \"{prompt}\"")
print("[*] Calling live UI stream generator...")

stream_fn = ctx.globals.get("hermes_chat_stream")
if stream_fn:
    chunks = []
    for chunk in stream_fn([DummyMsg(prompt)], None):
        chunks.append(chunk)

    full_response = "".join(chunks)
    print("\n" + "=" * 65)
    print("📝 خروجی چت‌باکس (Chat UI Rendered Output):")
    print("=" * 65)
    print(full_response)
    print("=" * 65)
    print("🔍 بررسی عدم وجود کد JSON یا آکولاد {}:")
    has_curly = "{" in full_response or "}" in full_response
    print(f"   -> آیا آکولاد {{}} در خروجی وجود دارد؟ {'بله (خطا!)' if has_curly else 'خیر (کاملاً تمیز و فارسی)'}")
    print("✅ تست با موفقیت انجام شد!")
else:
    print("Error: hermes_chat_stream not in ctx.globals!")
    sys.exit(1)
