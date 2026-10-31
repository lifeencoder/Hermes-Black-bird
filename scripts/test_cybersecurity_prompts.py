import sys
import io
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from client.model_client import ModelClient
from runner.agent_runner import AgentRunner
from tools.registry import ToolRegistry
from tools.mcp_client import MCPClient

# Connect to benchmark tools server
mcp_server_script = repo_root / "tests" / "benchmark_150_tools_server.py"
client_mcp = MCPClient(
    command=sys.executable,
    args=[str(mcp_server_script)],
    startup_timeout=25.0
)
client_mcp.start()

registry = ToolRegistry()
registry.register_mcp_tools(client_mcp)
print(f"[*] Registered {len(registry.get_tools())} tools.")

model_client = ModelClient(
    base_url="http://127.0.0.1:8000/v1",
    api_key="EMPTY",
    model_name="NousResearch/Hermes-3-Llama-3.1-70B-FP8"
)

runner = AgentRunner(
    model_client=model_client,
    tool_registry=registry,
    max_iterations=5
)

test_prompts = [
    (
        "آسیب‌پذیری تزریق SQL (SQL Injection)",
        "آسیب‌پذیری تزریق SQL را در یک سیستم لاگین تحلیل کن و نحوه جلوگیری از آن با Prepared Statements در پایتون را با ابزار دیتابیس تست کن."
    ),
    (
        "ممیزی سطوح دسترسی فرآیند (Process Security Audit)",
        "با ابزار execute_command شناسه کاربری و سطوح دسترسی (id و whoami) را بررسی و خطرات اجرای سرویس با دسترسی روت را تحلیل نما."
    ),
    (
        "امنیت رمزنگاری و توکن‌ها (Cryptographic Verification)",
        "یک تحلیل امنیتی از مبهم‌سازی با Base64 و هشینگ SHA-256 ارائه بده و با str_sha256 هش 'Admin-Session-Secure-Token-2026' را محاسبه کن."
    ),
    (
        "کنترل نرخ و دفاع در برابر Brute-Force (Rate Limiting)",
        "مکانیزم دفاعی در برابر حملات Brute-Force و DoS را بر روی اندپوینت‌های لاگین با الگوریتم Token Bucket در پایتون شبیه‌سازی کن."
    )
]

print("\n" + "=" * 70)
print("🛡️ RUNNING SPECIALIZED CYBERSECURITY PROMPT EVALUATIONS")
print("=" * 70)

for idx, (title, prompt) in enumerate(test_prompts, 1):
    print(f"\n--- [تست {idx}]: {title} ---")
    print(f"[*] پرسش: {prompt}")
    
    result = runner.run(
        messages=[{"role": "user", "content": prompt}],
        verbose=False,
        temperature=0.7,
        top_p=0.95
    )
    
    content = result.get("content", "") if isinstance(result, dict) else str(result)
    print(f"[+] پاسخ مدل دریافت شد ({len(content)} کاراکتر):\n")
    print(content[:350] + "...\n[ادامه پاسخ کامل]")
    print("-" * 50)

print("\n[+] تمامی پرامپت‌های امنیتی با موفقیت اجرا و ارزیابی شدند.")
client_mcp.close()
