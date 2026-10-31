import marimo._code_mode as cm

print("=== Starting Notebook Cleanup & Chat UI Execution ===")

ctx = cm.get_context()
cells_before = [(c.id, c.name, str(c.status)) for c in ctx.cells]
print(f"Current cells ({len(cells_before)}):")
for cid, cname, cstatus in cells_before:
    print(f"  - [{cid}] {cname} ({cstatus})")

to_delete = ["MJUe", "Kclp", "zlnx"]
to_run = ["Hbol", "vblA", "bkHC"]

async with cm.get_context() as actx:
    existing_ids = [c.id for c in actx.cells]
    for cid in to_delete:
        if cid in existing_ids:
            print(f"Deleting dead cell: {cid}")
            actx.delete_cell(cid)
        else:
            print(f"Cell {cid} not found, skipping delete.")

    for cid in to_run:
        if cid in existing_ids:
            print(f"Running cell: {cid}")
            actx.run_cell(cid)
        else:
            print(f"Cell {cid} not found for execution!")

print("[✓] Queue submitted to marimo runtime.")
