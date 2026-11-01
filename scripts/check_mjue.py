import marimo._code_mode as cm

ctx = cm.get_context(skip_staleness_check=True)
cell = next((c for c in ctx.cells if c.id == "MJUe"), None)
if cell:
    print("=== CELL MJUe CODE ===")
    print(cell.code)
