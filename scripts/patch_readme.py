import re

with open("README.md", "r", encoding="utf-8") as f:
    text = f.read()

# Clean up broken text
text = re.sub(r"---\s*\n+---\s*\n+## ⚡ راه‌اندازی سریع و پایداری سرور[\s\S]*?## 🛠️ تکنولوژی‌های مورد استفاده", "## 🛠️ تکنولوژی‌های مورد استفاده", text)

section = """---

## ⚡ راه‌اندازی سریع و پایداری سرور (MoLab Persistent Automation)

این مخزن برای محیط‌های ابری مانند MoLab بهینه‌سازی شده است که در هر بار راه‌اندازی مجدد، فایل‌های دایرکتوری جاری ماندگار هستند:

- **محیط‌های مجازی ماندگار (Persistent Virtualenvs):**
  - سرور vLLM در مسیر `/marimo/venvs/vllm` با نسخه `vllm==0.32.0` مستقر است.
  - سرور HexStrike AI در مسیر `/marimo/hexstrike-ai/venv` با تمامی پکیج‌های مورد نیاز آماده است.
- **کش ماندگار مدل (Persistent Model Cache):**
  - وزن‌های مدل `NousResearch/Hermes-3-Llama-3.1-70B-FP8` در پوشه `/marimo/hf_cache` ذخیره شده و نیازی به دانلود مجدد پس از ریستارت کانتینر نیست.
- **اسکریپت‌های تک‌دستوری:**
  - `bash /marimo/start.sh`: بررسی و روشن کردن فوری سرورهای HexStrike (پورت ۸۸۸۸) و vLLM (پورت ۸۰۰۰).
  - `bash /marimo/bootstrap.sh`: اسکریپت جامع بررسی سلامت پکیج‌ها، بازسازی خودکار در صورت نیاز و اجرای سرویس‌ها.

---

## 🛠️ تکنولوژی‌های مورد استفاده"""

text = text.replace("## 🛠️ تکنولوژی‌های مورد استفاده", section)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(text)

print("Cleanly updated README.md")
