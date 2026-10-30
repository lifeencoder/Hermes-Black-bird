#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hermes Black Bird - Enterprise Mock MCP Server
Provides 11 diverse, safe, and realistic tools across data storage, text processing,
mathematics, and diagnostics for benchmarking MCP client scalability and schema discovery.
Compatible with both MCP 1.x (FastMCP) and MCP 2.x (MCPServer) over stdio.
"""

import hashlib
import json
import os
import platform
import sqlite3
import statistics
import sys
import uuid
from typing import List, Optional

try:
    from mcp.server.fastmcp import FastMCP as ServerClass
except ImportError:
    from mcp.server.mcpserver import MCPServer as ServerClass

server = ServerClass("EnterpriseMockServer")


# ------------------------------------------------------------------------------
# 1. File & Data Tools
# ------------------------------------------------------------------------------
@server.tool(
    name="read_text_file",
    description="خواندن خطوط یک فایل متنی با اعمال سقف تعداد خطوط مجاز."
)
def read_text_file(filepath: str, max_lines: int = 50) -> str:
    if not os.path.exists(filepath):
        return f"خطا: فایل '{filepath}' یافت نشد."
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            lines = [f.readline() for _ in range(max_lines)]
        return "".join(lines)
    except Exception as err:
        return f"خطا در خواندن فایل: {err}"


@server.tool(
    name="query_sqlite",
    description="اجرای کوئری‌های استاندارد SELECT روی دیتابیس لوکال SQLite یا حافظه رم."
)
def query_sqlite(query: str, db_path: str = ":memory:") -> str:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [d[0] for d in cursor.description] if cursor.description else []
        conn.close()
        return json.dumps({"columns": columns, "rows": rows}, ensure_ascii=False)
    except Exception as err:
        return json.dumps({"error": str(err)}, ensure_ascii=False)


# ------------------------------------------------------------------------------
# 2. Text Analytics & NLP Tools
# ------------------------------------------------------------------------------
@server.tool(
    name="count_text_stats",
    description="تحلیل آماری متن شامل تعداد کلمات، کاراکترها، خطوط و تخمین توکن‌ها."
)
def count_text_stats(text: str) -> str:
    chars = len(text)
    words = len(text.split())
    lines = len(text.splitlines())
    estimated_tokens = int(chars / 3.8) if chars > 0 else 0
    return json.dumps({
        "characters": chars,
        "words": words,
        "lines": lines,
        "estimated_tokens": estimated_tokens
    }, ensure_ascii=False)


@server.tool(
    name="format_json_data",
    description="اعتبارسنجی و زیباسازی رشته‌های ساختاریافته JSON با تورفتگی مشخص."
)
def format_json_data(raw_json: str, indent: int = 2) -> str:
    try:
        data = json.loads(raw_json)
        return json.dumps(data, indent=indent, ensure_ascii=False)
    except Exception as err:
        return f"فرمت JSON نامعتبر است: {err}"


@server.tool(
    name="hash_text",
    description="تولید هش امن رمزنگاری‌شده (SHA256, SHA512, MD5) از یک رشته متنی."
)
def hash_text(text: str, algorithm: str = "sha256") -> str:
    algo = algorithm.lower().strip()
    if algo == "sha256":
        return hashlib.sha256(text.encode("utf-8")).hexdigest()
    elif algo == "sha512":
        return hashlib.sha512(text.encode("utf-8")).hexdigest()
    elif algo == "md5":
        return hashlib.md5(text.encode("utf-8")).hexdigest()
    else:
        return f"الگوریتم پشتیبانی‌نشده: {algorithm}"


# ------------------------------------------------------------------------------
# 3. Math & Analytics Tools
# ------------------------------------------------------------------------------
@server.tool(
    name="calculate_statistics",
    description="محاسبه شاخص‌های آماری توصیفی (میانگین، میانه، واریانس، کمینه و بیشینه) برای آرایه‌ای از اعداد."
)
def calculate_statistics(numbers: List[float]) -> str:
    if not numbers:
        return json.dumps({"error": "لیست اعداد خالی است."}, ensure_ascii=False)
    try:
        stats = {
            "count": len(numbers),
            "mean": statistics.mean(numbers),
            "median": statistics.median(numbers),
            "min": min(numbers),
            "max": max(numbers),
            "variance": statistics.variance(numbers) if len(numbers) > 1 else 0.0,
        }
        return json.dumps(stats, ensure_ascii=False)
    except Exception as err:
        return json.dumps({"error": str(err)}, ensure_ascii=False)


@server.tool(
    name="convert_temperature",
    description="تبدیل واحد دما بین سلسیوس (C)، فارنهایت (F) و کلوین (K)."
)
def convert_temperature(value: float, from_unit: str, to_unit: str) -> str:
    u_from = from_unit.upper().strip()
    u_to = to_unit.upper().strip()

    if u_from == "C":
        celsius = value
    elif u_from == "F":
        celsius = (value - 32) * 5 / 9
    elif u_from == "K":
        celsius = value - 273.15
    else:
        return f"واحد مبدأ نامعتبر: {from_unit}"

    if u_to == "C":
        res = celsius
    elif u_to == "F":
        res = (celsius * 9 / 5) + 32
    elif u_to == "K":
        res = celsius + 273.15
    else:
        return f"واحد مقصد نامعتبر: {to_unit}"

    return f"{value} {u_from} = {round(res, 2)} {u_to}"


# ------------------------------------------------------------------------------
# 4. System & Diagnostics Tools
# ------------------------------------------------------------------------------
@server.tool(
    name="get_system_health",
    description="ارزیابی سلامت و منابع سیستم‌عامل شامل پلتفرم، تعداد هسته‌های پردازشی و مفسر پایتون."
)
def get_system_health() -> str:
    return json.dumps({
        "status": "healthy",
        "system": platform.system(),
        "release": platform.release(),
        "architecture": platform.machine(),
        "cpu_count": os.cpu_count(),
        "python_version": sys.version.split()[0],
    }, ensure_ascii=False)


@server.tool(
    name="generate_uuid",
    description="تولید شناسه منحصربه‌فرد تصادفی استاندارد UUID نسخه ۴."
)
def generate_uuid() -> str:
    return str(uuid.uuid4())


@server.tool(
    name="inspect_environment_variables",
    description="بررسی نام کلیدهای متغیرهای محیطی با فیلتر پیشوند مشخص (بدون نمایش مقادیر حساس)."
)
def inspect_environment_variables(prefix: str = "") -> str:
    keys = [k for k in os.environ.keys() if k.upper().startswith(prefix.upper())]
    return json.dumps({"matched_keys": sorted(keys), "total": len(keys)}, ensure_ascii=False)


@server.tool(
    name="echo_message",
    description="بازگرداندن پیام ورودی به همراه برچسب زمانی سرور جهت تست پینگ و تأخیر ارتباطی."
)
def echo_message(message: str) -> str:
    import time
    return f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] سرور MCP دریافت کرد: {message}"


if __name__ == "__main__":
    server.run(transport="stdio")
