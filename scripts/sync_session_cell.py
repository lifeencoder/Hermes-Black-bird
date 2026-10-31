import marimo._code_mode as cm
import textwrap
import re

with open("/marimo/notebook.py", "r", encoding="utf-8") as f:
    nb_code = f.read()

match = re.search(r"def persian_chat_app\([^\)]*\):\n([\s\S]*?)(?=\n    return|\nif __name__|$)", nb_code)
if not match:
    raise RuntimeError("Failed to match persian_chat_app")

body = match.group(1)
unindented_body = textwrap.dedent(body)
if not unindented_body.strip().endswith("_main_layout"):
    unindented_body += "\n_main_layout\n"

print(f"Extracted cell body ({len(unindented_body)} chars)")

async with cm.get_context(skip_staleness_check=True) as ctx:
    app_cell = next((c for c in ctx.cells if c.name == "persian_chat_app" or "hermes_chat_stream" in c.code or c.id == "rttW"), None)
    if app_cell:
        print(f"Editing existing cell {app_cell.id}...")
        ctx.edit_cell(app_cell.id, code=unindented_body)
        target_id = app_cell.id
    else:
        print("Creating new cell persian_chat_app after MJUe...")
        res = ctx.create_cell(code=unindented_body, after="MJUe", name="persian_chat_app")
        target_id = res if isinstance(res, str) else res.id

    print(f"Running cell {target_id}...")
    ctx.run_cell("Hbol")
    ctx.run_cell("MJUe")
    ctx.run_cell(target_id)
    print("All cells executed successfully!")
