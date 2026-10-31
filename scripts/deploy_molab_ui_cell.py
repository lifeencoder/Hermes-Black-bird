import marimo._code_mode as cm
import re

# Read notebook.py from /marimo/notebook.py
with open("/marimo/notebook.py", "r", encoding="utf-8") as f:
    nb_code = f.read()

# Extract persian_chat_app code
# It starts at def persian_chat_app and goes to return
match = re.search(r"@app\.cell\(hide_code=True\)\ndef persian_chat_app\([\s\S]*?(?=\nif __name__|$)", nb_code)
if not match:
    raise RuntimeError("Could not find persian_chat_app in /marimo/notebook.py")

cell_full_code = match.group(0)
# Strip @app.cell(hide_code=True)\ndef persian_chat_app(...) and extract cell body or marimo cell code
# Wait, in marimo._code_mode, cell code is the python function body, or the function definition?
# Let's check how marimo stores cell code!
print("Extracted cell definition.")

# Let's inspect existing cell MJUe to see how its code is formatted
ctx = cm.get_context(skip_staleness_check=True)
mjue = next((c for c in ctx.cells if c.id == "MJUe"), None)
if mjue:
    print("MJUe code preview:")
    print(repr(mjue.code[:150]))
