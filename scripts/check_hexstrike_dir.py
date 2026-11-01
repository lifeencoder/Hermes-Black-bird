import os
import subprocess

print("Contents of /marimo/hexstrike-ai:")
if os.path.exists("/marimo/hexstrike-ai"):
    for x in sorted(os.listdir("/marimo/hexstrike-ai")):
        print(" ", x)
else:
    print("/marimo/hexstrike-ai DOES NOT EXIST!")
