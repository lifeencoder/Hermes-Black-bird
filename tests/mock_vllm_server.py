#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lightweight Mock vLLM OpenAI-Compatible Server for Local Behavioral & Integration Testing.
Listens on port 8000 and serves /v1/models and /v1/chat/completions.
Provides intelligent, conversational, dynamic dispatching for greetings, coding, math,
cybersecurity, and system diagnostics without repetitive static fallbacks.
"""

import sys
import io
import re

# Force UTF-8 stdout/stderr on Windows to prevent UnicodeEncodeError
if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except Exception:
        pass

import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

MODEL_ID = "NousResearch/Hermes-3-Llama-3.1-70B-FP8"

class MockVLLMHandler(BaseHTTPRequestHandler):
    def _send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def do_GET(self):
        if self.path in ("/v1/models", "/models"):
            self._send_json(200, {
                "object": "list",
                "data": [
                    {
                        "id": MODEL_ID,
                        "object": "model",
                        "created": int(time.time()),
                        "owned_by": "vllm"
                    }
                ]
            })
        else:
            self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        if self.path not in ("/v1/chat/completions", "/chat/completions"):
            self._send_json(404, {"error": "Not found"})
            return

        content_len = int(self.headers.get("Content-Length", 0))
        req_body = self.rfile.read(content_len).decode("utf-8")
        data = json.loads(req_body)

        messages = data.get("messages", [])
        temp = data.get("temperature", 0.7)

        # Extract latest user message
        user_msgs = [m for m in messages if m.get("role") == "user"]
        last_user_prompt = user_msgs[-1].get("content", "").strip() if user_msgs else ""
        prompt_lower = last_user_prompt.lower()

        try:
            print(f"[vLLM Mock] Request prompt: '{last_user_prompt[:60]}...'", flush=True)
        except Exception:
            pass

        # Check if there is already a tool message in the conversation
        has_tool_response = any(m.get("role") == "tool" for m in messages)

        # ----------------------------------------------------------------------
        # Turn 1: Check if prompt requires immediate conversational answer OR a tool call
        # ----------------------------------------------------------------------
        if not has_tool_response:
            # 1. Greetings (سلام، درود، چطوری و...) -> Direct answer, NO tool needed!
            greetings = ["سلام", "درود", "صبح بخیر", "عصر بخیر", "شب بخیر", "سلامت باشی", "خوبی", "چطوری", "سلام علیکم"]
            is_greeting = any(prompt_lower == g or prompt_lower.startswith(g + " ") for g in greetings)
            
            if is_greeting:
                direct_answer = (
                    "سلام و درود بر شما! من دستیار هوشمند هرمس (Hermes-3) هستم.\n\n"
                    "سامانه به طور کامل آماده و به رجیستری ۱۶۵ ابزار محلی متصل است. "
                    "می‌توانید هر نوع سوال علمی، درخواست کدنویسی پایتون، تحلیل امنیتی، محاسبات ریاضی یا اجرای ابزارهای سیستمی را بفرمایید تا انجام دهم."
                )
                self._send_direct_completion(direct_answer)
                return

            # 2. Identity & capabilities
            if any(k in prompt_lower for k in ["کی هستی", "معرفی کن", "چه کارهایی", "قابلیت", "راهنما"]):
                direct_answer = (
                    "### 🦅 سامانه دستیار هوشمند هرمس (Hermes-3 Llama-3.1-70B)\n\n"
                    "من یک مدل زبانی پیشرفته هستم که برای استدلال پیچیده، تعامل چندمرحله‌ای و اجرای مستقل ابزارها بهینه‌سازی شده‌ام.\n\n"
                    "**توانمندی‌های اصلی:**\n"
                    "۱. **تحلیل و نگارش کدهای نرم‌افزاری:** پایتون، شل لینوکس، SQL و معماری نرم‌افزار.\n"
                    "۲. **ممیزی و تحلیل امنیت سایبری:** ارزیابی آسیب‌پذیری‌های وب (مانند SQLi و XSS)، بررسی سطوح دسترسی فرآیندها و مکانیزم‌های رمزنگاری.\n"
                    "۳. **اجرای خودکار ابزارهای محلی (Tool Use):** یکپارچه با ۱۶۵ ابزار در حوزه‌های ریاضی، آمار، تبدیل واحد، دیتابیس و تله‌متری سیستم.\n\n"
                    "چه سناریو یا دستوری را مایلید با هم بررسی و اجرا کنیم؟"
                )
                self._send_direct_completion(direct_answer)
                return

            # 3. Dedicated Cybersecurity Tools:
            if any(k in prompt_lower for k in ["sql", "تزریق sql", "sqli", "دیتابیس", "database"]):
                tool_call = {
                    "id": "call_sqli_audit_001",
                    "type": "function",
                    "function": {
                        "name": "query_sqlite",
                        "arguments": json.dumps({
                            "query": "SELECT '1' as test_col, 'safe_parameterized_query' as status;"
                        })
                    }
                }
            elif any(k in prompt_lower for k in ["whoami", "id", "دسترسی", "شناسه کاربری", "root", "روت", "سطوح"]):
                tool_call = {
                    "id": "call_priv_audit_002",
                    "type": "function",
                    "function": {
                        "name": "execute_command",
                        "arguments": json.dumps({"command": "id"})
                    }
                }
            elif any(k in prompt_lower for k in ["brute", "ddos", "rate limit", "محدودیت", "حمله", "منع سرویس", "token bucket", "توکن باکت"]):
                tool_call = {
                    "id": "call_ratelimit_sim_004",
                    "type": "function",
                    "function": {
                        "name": "execute_command",
                        "arguments": json.dumps({
                            "command": "python -c \"import time; print('RateLimiter Status: 5 reqs processed, 0 dropped | Threshold: 10 req/min | State: ACTIVE')\""
                        })
                    }
                }
            elif any(k in prompt_lower for k in ["sha256", "sha-256", "هش", "hash", "امضا"]):
                text_to_hash = "Admin-Session-Secure-Token-2026"
                if "'" in last_user_prompt:
                    parts = last_user_prompt.split("'")
                    if len(parts) >= 3:
                        text_to_hash = parts[1]
                tool_call = {
                    "id": "call_crypto_hash_003",
                    "type": "function",
                    "function": {
                        "name": "str_sha256",
                        "arguments": json.dumps({"text": text_to_hash})
                    }
                }
            elif any(k in prompt_lower for k in ["سلامت", "health", "سخت‌افزار", "وضعیت سرور", "مشخصات سیستم"]):
                tool_call = {
                    "id": "call_sys_health_005",
                    "type": "function",
                    "function": {
                        "name": "get_system_health",
                        "arguments": json.dumps({})
                    }
                }
            elif any(k in prompt_lower for k in ["کد", "پایتون", "اسکریپت", "برنامه", "تابع"]):
                # Direct programming answer
                code_answer = (
                    f"### 💻 کد پایتون پیشنهادی برای: {last_user_prompt}\n\n"
                    "در ادامه پیاده‌سازی بهینه و استاندارد پایتون بر اساس بهترین الگوهای توسعه ارائه شده است:\n\n"
                    "```python\n"
                    "import os\n"
                    "import sys\n"
                    "from typing import List, Dict, Any\n\n"
                    "def process_task(input_data: Any) -> Dict[str, Any]:\n"
                    "    \"\"\"\n"
                    "    پردازش ساختاریافته داده‌ها همراه با مدیریت استثناها.\n"
                    "    \"\"\"\n"
                    "    try:\n"
                    "        result = {\n"
                    "            'status': 'success',\n"
                    "            'payload': input_data,\n"
                    "            'length': len(input_data) if hasattr(input_data, '__len__') else 1\n"
                    "        }\n"
                    "        return result\n"
                    "    except Exception as err:\n"
                    "        return {'status': 'error', 'message': str(err)}\n\n"
                    "if __name__ == '__main__':\n"
                    "    data = 'Hermes-3-Agent-Data'\n"
                    "    print(process_task(data))\n"
                    "```\n\n"
                    "✅ این اسکریپت با رعایت اصول Clean Code و Type Hinting نوشته شده و آماده اجرا در محیط پروژه است."
                )
                self._send_direct_completion(code_answer)
                return
            else:
                # Conversational general answer echoing user's prompt intelligently
                gen_answer = (
                    f"در پاسخ به پرسش شما در مورد «{last_user_prompt}»:\n\n"
                    "موضوع مطرح‌شده از دیدگاه فنی و تحلیلی قابل بررسی از چند جنبه است:\n\n"
                    "۱. **بررسی ساختاری:** برای رسیدن به بالاترین بهره‌وری، تفکیک اجزا و رعایت ماژولاریتی در اولویت است.\n"
                    "۲. **به‌کارگیری ابزارها:** در صورت تمایل، می‌توانیم از ابزارهای ۱۶۵ گانه محلی سرور (مانند تحلیل داده، توابع ریاضی یا دستورات سیستمی) برای پردازش خودکار این مورد استفاده کنیم.\n\n"
                    "آیا مایلید جزئیات بیشتری درباره این موضوع پیاده‌سازی کنیم یا ابزار خاصی را برای آن فراخوانی نمایم؟"
                )
                self._send_direct_completion(gen_answer)
                return

            resp = {
                "id": "chatcmpl-mock-turn1",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": MODEL_ID,
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": None,
                            "tool_calls": [tool_call]
                        },
                        "finish_reason": "tool_calls"
                    }
                ],
                "usage": {"prompt_tokens": 150, "completion_tokens": 40, "total_tokens": 190}
            }
            self._send_json(200, resp)

        # ----------------------------------------------------------------------
        # Turn 2: Synthesize deep analysis based on the tool result
        # ----------------------------------------------------------------------
        else:
            tool_msg = next((m for m in reversed(messages) if m.get("role") == "tool"), {})
            tool_out = tool_msg.get("content", "OK")

            if any(k in prompt_lower for k in ["sql", "تزریق sql", "sqli", "دیتابیس"]):
                persian_answer = (
                    "### 🛡️ تحلیل جامع آسیب‌پذیری تزریق SQL (SQL Injection) و راهکار دفاعی\n\n"
                    "آسیب‌پذیری **تزریق SQL (SQLi)** زمانی رخ می‌دهد که داده‌های ورودی کاربر بدون اعتبارسنجی یا پارامتریزه شدن، مستقیماً در رشته کوئری پایگاه‌داده الحاق شوند (String Concatenation). این امر مرز بین «کد دستوری» و «داده» را از بین می‌برد.\n\n"
                    "#### ۱. بردار حمله متداول (Vulnerable Code):\n"
                    "```python\n"
                    "# ❌ شیوه ناامن: الحاق مستقیم ورودی کاربر به کوئری\n"
                    "username = request.form['username']\n"
                    "password = request.form['password']\n"
                    "query = f\"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'\"\n"
                    "# پی‌لود نفوذگر: ' OR '1'='1' -- \n"
                    "```\n\n"
                    "#### ۲. پیاده‌سازی امن با Prepared Statements (کوئری‌های پارامتریزه):\n"
                    "در این روش، ساختار کوئری از قبل توسط موتور پایگاه‌داده کامپایل می‌شود و داده‌های کاربر به عنوان پارامترهای مستقل ارسال می‌گردند، بنابراین هرگز به عنوان کد SQL تفسیر نمی‌شوند:\n\n"
                    "```python\n"
                    "import sqlite3\n\n"
                    "def authenticate_user(username: str, password_hash: str):\n"
                    "    with sqlite3.connect('database.db') as conn:\n"
                    "        cursor = conn.cursor()\n"
                    "        # ✅ شیوه کاملاً امن: استفاده از کوئری پارامتریزه با علامت‌های جایگزین (?)\n"
                    "        query = \"SELECT id, username, role FROM users WHERE username = ? AND password_hash = ?\"\n"
                    "        cursor.execute(query, (username, password_hash))\n"
                    "        user = cursor.fetchone()\n"
                    "        return user\n"
                    "```\n\n"
                    f"#### ۳. ارزیابی امنیتی در محیط ایزوله:\n"
                    f"کوئری استاندارد پایگاه‌داده توسط ابزار `query_sqlite` در سرور تست اجرا شد و نتیجه زیر حاصل شد:\n"
                    f"```text\n{tool_out}\n```\n\n"
                    "#### ۴. اقدامات پیشگیرانه دفاع در عمق (Defense-in-Depth):\n"
                    "۱. **اعمال اصل حداقل اختیارات (Principle of Least Privilege):** حساب کاربری متصل به دیتابیس نباید دسترسی `DROP TABLE` یا `ALTER` داشته باشد.\n"
                    "۲. **استفاده از ORMهای مدرن:** استفاده از ابزارهایی مانند SQLAlchemy یا Django ORM که به صورت پیش‌فرض کوئری‌ها را ایمن می‌سازند.\n"
                    "۳. **استفاده از WAF (Web Application Firewall):** پایش امضای پی‌لودهای مخرب مانند `UNION SELECT` در لایه شبکه."
                )

            elif any(k in prompt_lower for k in ["whoami", "id", "دسترسی", "شناسه کاربری", "root", "روت", "سطوح"]):
                persian_answer = (
                    "### 🔍 گزارش ممیزی امنیتی سطوح دسترسی فرآیند (Process Security Audit)\n\n"
                    "بررسی هویت فرآیند و تفکیک دسترسی‌ها (Principle of Least Privilege) یکی از پایه‌ای‌ترین الزامات امنیت سیستم‌های سروری است.\n\n"
                    f"#### ۱. نتیجه ممیزی زنده هویت و دسترسی‌ها:\n"
                    f"ابزار امنیتی `execute_command` برای استعلام هویت پروسس اجرا شد:\n"
                    f"```text\n{tool_out}\n```\n\n"
                    "#### ۲. تحلیل امنیتی خروجی:\n"
                    "خروجی نشان می‌دهد پروسس با شناسه کاربری غیر روت (`uid=1000`) و بدون عضویت در گروه‌های دارای حق صدور `sudo` در حال اجراست. این وضعیت به عنوان یک **بهروش امنیتی (Security Best Practice)** تلقی می‌شود.\n\n"
                    "#### ۳. خطرات مهلک اجرای سرویس‌ها با دسترسی Root / Administrator:\n"
                    "- **فرار از کانتینر (Container Breakout):** در صورت رخداد RCE (Remote Code Execution) روی سرویسی با دسترسی Root، نفوذگر دسترسی کامل به تمامی فایل‌های کرنل و هاست پیدا می‌کند.\n"
                    "- **تخریب یکپارچگی سیستم:** امکان دستکاری لاگ‌های سیستمی (`/var/log`) و پنهان‌سازی فعالیت‌های مهاجم.\n"
                    "- **آلودگی کل شبکه:** امکان نصب Rootkit و فعال‌سازی پروتکل‌های شنود ترافیک (Sniffing) روی اینترفیس‌های شبکه.\n\n"
                    "#### ۴. چک‌لیست ایمن‌سازی سرور:\n"
                    "```bash\n"
                    "# ایجاد کاربر اختصاصی بدون شل لاگین برای سرویس\n"
                    "useradd -r -s /usr/sbin/nologin hermes-service\n\n"
                    "# محدودسازی دسترسی فایل‌های تنظیمات به کاربر سرویس\n"
                    "chown -R hermes-service:hermes-service /opt/hermes-service\n"
                    "chmod 750 /opt/hermes-service\n"
                    "```"
                )

            elif any(k in prompt_lower for k in ["brute", "ddos", "rate limit", "محدودیت", "حمله", "منع سرویس", "token bucket", "توکن باکت"]):
                persian_answer = (
                    "### 🛡️ معماری دفاعی در برابر حملات Brute-Force و DoS با مکانیزم Rate Limiting\n\n"
                    "حملات حدس رمز عبور (Brute-Force) و پر کردن اعتبارنامه‌ها (Credential Stuffing) متداول‌ترین روش‌های تسخیر حساب‌های کاربری هستند. کنترل نرخ درخواست‌ها (Rate Limiting) نخستین سد دفاعی برنامه است.\n\n"
                    f"#### ۱. نتیجه وضعیت ماژول Rate Limiter در سرور:\n"
                    f"```text\n{tool_out}\n```\n\n"
                    "#### ۲. پیاده‌سازی الگوریتم Token Bucket در پایتون:\n"
                    "این الگوریتم اجازه ارسال انفجاری کوتاه‌مدت (Burst) تا ظرفیت باکت را می‌دهد، در حالی که نرخ میانگین را به شدت کنترل می‌کند:\n\n"
                    "```python\n"
                    "import time\n\n"
                    "class TokenBucketRateLimiter:\n"
                    "    def __init__(self, capacity: int, fill_rate: float):\n"
                    "        \"\"\"\n"
                    "        capacity: حداکثر توکن‌های موجود در باکت\n"
                    "        fill_rate: تعداد توکن‌های اضافه‌شده در هر ثانیه\n"
                    "        \"\"\"\n"
                    "        self.capacity = capacity\n"
                    "        self.fill_rate = fill_rate\n"
                    "        self.tokens = capacity\n"
                    "        self.last_update = time.time()\n\n"
                    "    def allow_request(self, tokens_needed: int = 1) -> bool:\n"
                    "        now = time.time()\n"
                    "        elapsed = now - self.last_update\n"
                    "        self.last_update = now\n"
                    "        # شارژ مجدد باکت\n"
                    "        self.tokens = min(self.capacity, self.tokens + elapsed * self.fill_rate)\n\n"
                    "        if self.tokens >= tokens_needed:\n"
                    "            self.tokens -= tokens_needed\n"
                    "            return True\n"
                    "        return False\n"
                    "```\n\n"
                    "#### ۳. هدرهای استاندارد امنیتی پاسخ وب:\n"
                    "هنگام اعمال محدودیت نرخ و حفاظت از اندپوینت‌ها، هدرهای زیر باید به کلاینت بازگردانده شوند:\n"
                    "- `X-RateLimit-Limit`: حداکثر تعداد درخواست‌های مجاز در بازه زمانی.\n"
                    "- `X-RateLimit-Remaining`: تعداد درخواست‌های باقی‌مانده در پنجره فعلی.\n"
                    "- `Retry-After`: مدت زمان ثانیه که کلاینت باید پیش از ارسال مجدد صبر کند.\n"
                    "- `Content-Security-Policy (CSP)`: جلوگیری از بارگذاری اسکریپت‌های ناشناس.\n"
                    "- `Strict-Transport-Security (HSTS)`: اجبار ارتباط امن با پروتکل HTTPS."
                )

            elif any(k in prompt_lower for k in ["sha256", "sha-256", "هش", "hash", "امضا"]):
                persian_answer = (
                    "### 🔐 تحلیل امنیت رمزنگاری: مبهم‌سازی داده‌ها در برابر توابع هش یک‌طرفه\n\n"
                    "در مهندسی امنیت نرم‌افزار، تفکیک دقیق میان مفاهیم **کدگذاری (Encoding)**، **رمزنگاری (Encryption)** و **درهم‌سازی (Hashing)** بسیار حیاتی است.\n\n"
                    "#### ۱. مقایسه مفهومی مبهم‌سازی با Base64 و هشینگ:\n"
                    "- **الگوریتم Base64:** صرفاً یک قالب کدگذاری باینری به متن است؛ دارای هیچ کلید محرمانه‌ای نبوده و هر فردی می‌تواند با `base64_decode` آن را فوراً به حالت اولیه برگرداند. بنابراین **هیچ امنیتی ایجاد نمی‌کند**.\n"
                    "- **تابع هش SHA-256:** یک تابع ریاضی یک‌طرفه و غیرقابل بازگشت است که خروجی ۲۵۶ بیتی (۶۴ کاراکتر هگزادسیمال) تولید می‌کند و خاصیت مقاومت در برابر تصادم (Collision Resistance) دارد.\n\n"
                    f"#### ۲. محاسبه مقدار هش امنیتی:\n"
                    f"با فراخوانی ابزار `str_sha256` روی توکن هدف، هش قطعی زیر محاسبه گردید:\n"
                    f"```text\nSHA256: {tool_out}\n```\n\n"
                    "#### ۳. پیاده‌سازی مکانیزم اعتبارسنجی توکن‌ها با HMAC:\n"
                    "برای اطمینان از اینکه توکن نشست توسط نفوذگر دستکاری نشده باشد، از **HMAC-SHA256** با کلید سرور استفاده می‌شود:\n\n"
                    "```python\n"
                    "import hmac\n"
                    "import hashlib\n\n"
                    "SECRET_KEY = b\"hermes-enterprise-ultra-secure-key-2026\"\n\n"
                    "def generate_signed_token(payload: str) -> str:\n"
                    "    signature = hmac.new(SECRET_KEY, payload.encode('utf-8'), hashlib.sha256).hexdigest()\n"
                    "    return f\"{payload}.{signature}\"\n\n"
                    "def verify_signed_token(signed_token: str) -> bool:\n"
                    "    try:\n"
                    "        payload, signature = signed_token.rsplit('.', 1)\n"
                    "        expected = hmac.new(SECRET_KEY, payload.encode('utf-8'), hashlib.sha256).hexdigest()\n"
                    "        # استفاده از compare_digest برای جلوگیری از حملات زمان‌بندی (Timing Attacks)\n"
                    "        return hmac.compare_digest(signature, expected)\n"
                    "    except ValueError:\n"
                    "        return False\n"
                    "```\n\n"
                    "✅ **نکته کلیدی:** با استفاده از `hmac.compare_digest`، حمله کانال جانبی زمان‌بندی (Timing Attack) خنثی می‌گردد."
                )

            elif any(k in prompt_lower for k in ["سلامت", "health", "سخت‌افزار", "وضعیت سرور", "مشخصات سیستم"]):
                persian_answer = (
                    "### 📋 گزارش بررسی وضعیت سلامت و پایداری سیستم\n\n"
                    f"نتیجه استعلام تله‌متری سیستم‌عامل و مفسر پایتون توسط ابزار اختصاصی:\n\n"
                    f"```json\n{tool_out}\n```\n\n"
                    "✅ **نتیجه ارزیابی:** سرور در وضعیت پایدار (Healthy) بوده و تمامی کانال‌های اجرایی مهیای دریافت دستورات هستند."
                )

            else:
                persian_answer = (
                    f"نتیجه فراخوانی ابزار مربوط به «{last_user_prompt}»:\n\n"
                    f"```text\n{tool_out}\n```\n\n"
                    "عملیات با موفقیت در محیط ایزوله سرور اجرا و ارزیابی شد."
                )

            self._send_direct_completion(persian_answer)

    def _send_direct_completion(self, content_text):
        resp = {
            "id": f"chatcmpl-mock-{int(time.time()*1000)}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": MODEL_ID,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": content_text
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {"prompt_tokens": 100, "completion_tokens": len(content_text)//4, "total_tokens": 100 + len(content_text)//4}
        }
        self._send_json(200, resp)

    def log_message(self, format, *args):
        pass

def run_server(port=8000):
    server = HTTPServer(("0.0.0.0", port), MockVLLMHandler)
    print(f"[+] Mock vLLM server running on http://127.0.0.1:{port}/v1", flush=True)
    server.serve_forever()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)
