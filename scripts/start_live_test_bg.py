import subprocess

# Launch /marimo/run_live_test.py detached
log_file = open('/marimo/live_test.log', 'w', encoding='utf-8')
p = subprocess.Popen(
    ['/tmp/uv-venv/bin/python', '/marimo/run_live_test.py'],
    start_new_session=True,
    stdout=log_file,
    stderr=subprocess.STDOUT,
    stdin=subprocess.DEVNULL
)
print("Started run_live_test.py detached with PID:", p.pid)
