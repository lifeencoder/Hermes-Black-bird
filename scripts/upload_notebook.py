import os
import sys
import base64

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from remote_exec import run_code

with open("notebook.py", "rb") as f:
    b64_data = base64.b64encode(f.read()).decode("ascii")

remote_script = f"""import base64
with open('/marimo/notebook.py', 'wb') as f:
    f.write(base64.b64decode('{b64_data}'))
print('[✓] notebook.py written successfully.')
"""

run_code(remote_script)
