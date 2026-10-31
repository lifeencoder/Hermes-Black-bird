import marimo._code_mode as cm

ctx = cm.get_context(skip_staleness_check=True)
print("=== MOLAB CELLS ===")
for c in ctx.cells:
    print(f"Cell ID: {c.id}, Name: {c.name}")
