import subprocess

print("=== DETAILED PROCESS LIST ===")
print(subprocess.getoutput("ps -eo pid,ppid,user,args | head -n 30"))
