import subprocess

print("=== VERIFYING VLLM IN PERSISTENT VENV ===")
vllm_py = "/marimo/venvs/vllm/bin/python"
cmd = f"{vllm_py} -c 'import vllm, torch; print(\"vLLM version:\", vllm.__version__, \"| PyTorch:\", torch.__version__, \"| CUDA:\", torch.cuda.is_available())'"
print(subprocess.getoutput(cmd))
