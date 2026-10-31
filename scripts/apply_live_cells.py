import marimo._code_mode as cm
import ast
import textwrap

with open('/marimo/notebook.py', 'r', encoding='utf-8') as f:
    notebook_content = f.read()

tree = ast.parse(notebook_content)
cell_codes = {}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in ('env_check', 'persian_chat_settings', 'persian_chat_app'):
        # Filter out trailing Return node if present
        stmts = [s for s in node.body if not isinstance(s, ast.Return)]
        lines = notebook_content.splitlines()[stmts[0].lineno - 1 : stmts[-1].end_lineno]
        code = textwrap.dedent('\n'.join(lines))
        cell_codes[node.name] = code
        print(f"Cell {node.name} has {len(code)} chars, ends with: {code.splitlines()[-1]}")

async with cm.get_context() as ctx:
    print("Updating cell Hbol...")
    ctx.edit_cell('Hbol', code=cell_codes['env_check'])
    print("Updating cell MJUe...")
    ctx.edit_cell('MJUe', code=cell_codes['persian_chat_settings'])
    print("Updating cell vblA...")
    ctx.edit_cell('vblA', code=cell_codes['persian_chat_app'])
    print("Queuing runs...")
    ctx.run_cell('Hbol')
    ctx.run_cell('MJUe')
    ctx.run_cell('vblA')

print("Successfully compiled and queued all cells!")
