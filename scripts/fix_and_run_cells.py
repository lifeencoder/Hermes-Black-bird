import marimo._code_mode as cm

async with cm.get_context(skip_staleness_check=True) as ctx:
    cell_mjue = next((c for c in ctx.cells if c.id == "MJUe"), None)
    if cell_mjue:
        new_code = "import marimo as mo\n" + cell_mjue.code.replace("import marimo as mo\n", "")
        ctx.edit_cell("MJUe", code=new_code)
        print("Updated MJUe with import marimo as mo")
    
    print("Running MJUe...")
    ctx.run_cell("MJUe")
    print("Running vblA...")
    ctx.run_cell("vblA")
    print("All cells executed successfully!")
