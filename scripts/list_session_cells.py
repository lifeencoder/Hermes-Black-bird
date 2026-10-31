import marimo._code_mode as cm

ctx = cm.get_context()
for c in ctx.cells:
    print(f"Cell ID: {c.id}, Name: {c.name}")
