import torch
import subprocess

print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("Device:", torch.cuda.get_device_name(0))
    print("Device count:", torch.cuda.device_count())

print("\nCheck uv cache & wheel cache:")
print(subprocess.getoutput("uv cache dir"))
print(subprocess.getoutput("ls -la $(uv cache dir)"))
