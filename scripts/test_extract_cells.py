import marimo._code_mode as cm
import ast

# 1. Read /marimo/notebook.py
with open('/marimo/notebook.py', 'r', encoding='utf-8') as f:
    notebook_content = f.read()

# 2. Extract function bodies for cells
tree = ast.parse(notebook_content)

cell_codes = {}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in ('env_check', 'persian_chat_settings', 'persian_chat_app'):
        # Get source segment
        lines = notebook_content.splitlines()[node.body[0].lineno - 1 : node.body[-1].end_lineno]
        # Dedent
        import textwrap
        code = textwrap.dedent('\n'.join(lines))
        cell_codes[node.name] = code
        print(f"Extracted {node.name}: {len(code)} chars")

print("Cells extracted:", list(cell_codes.keys()))
