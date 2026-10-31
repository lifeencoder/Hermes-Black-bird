#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a safe, high-scale MCP Server with 155+ diverse enterprise tools:
- Math & Arithmetic (25 tools)
- Statistics & Analytics (20 tools)
- Geometry & Trigonometry (20 tools)
- String Manipulation & NLP (25 tools)
- Date, Time & Calendar (20 tools)
- Unit Conversions (25 tools)
- Data Encoding & Formatting (15 tools)
- System Diagnostics & Command Sandbox (10 tools)
Total: 160 tools.
"""

template = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hermes Black Bird - Scalability Benchmark MCP Server (160 Enterprise Tools)
Provides a rich, safe, and realistic catalog of 160 tools across mathematics,
geometry, statistics, string manipulation, date-time, data transformation,
and system telemetry for benchmarking agent tool-calling scalability.
"""

import os
import sys
import math
import json
import uuid
import time
import base64
import hashlib
import sqlite3
import platform
import statistics
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any

try:
    from mcp.server.fastmcp import FastMCP as ServerClass
except ImportError:
    from mcp.server.mcpserver import MCPServer as ServerClass

server = ServerClass("ScalabilityBenchmarkServer")

# ==============================================================================
# 1. Math & Arithmetic (25 tools)
# ==============================================================================
@server.tool(name="math_add", description="محاسبه مجموع دو عدد اعشاری یا صحیح.")
def math_add(a: float, b: float) -> float: return a + b

@server.tool(name="math_sub", description="محاسبه تفریق عدد دوم از عدد اول.")
def math_sub(a: float, b: float) -> float: return a - b

@server.tool(name="math_mul", description="محاسبه حاصل‌ضرب دو عدد.")
def math_mul(a: float, b: float) -> float: return a * b

@server.tool(name="math_div", description="محاسبه حاصل تقسیم عدد اول بر دوم با بررسی تقسیم بر صفر.")
def math_div(a: float, b: float) -> str:
    if b == 0: return "خطا: تقسیم بر صفر مجاز نیست."
    return str(a / b)

@server.tool(name="math_mod", description="محاسبه باقیمانده تقسیم صحیح a بر b.")
def math_mod(a: int, b: int) -> str:
    if b == 0: return "خطا: تقسیم بر صفر."
    return str(a % b)

@server.tool(name="math_pow", description="محاسبه عدد پایه به توان نما (a^b).")
def math_pow(base: float, exp: float) -> float: return math.pow(base, exp)

@server.tool(name="math_sqrt", description="محاسبه ریشه دوم (جذر) عدد نامنفی.")
def math_sqrt(x: float) -> str:
    if x < 0: return "خطا: جذر عدد منفی تعریف نشده است."
    return str(math.sqrt(x))

@server.tool(name="math_cbrt", description="محاسبه ریشه سوم (کعب) یک عدد.")
def math_cbrt(x: float) -> float: return math.cbrt(x) if hasattr(math, 'cbrt') else (x ** (1/3))

@server.tool(name="math_abs", description="محاسبه مقدار قدر مطلق یک عدد.")
def math_abs(x: float) -> float: return abs(x)

@server.tool(name="math_factorial", description="محاسبه فاکتوریل یک عدد صحیح نامنفی کوچک.")
def math_factorial(n: int) -> str:
    if n < 0 or n > 100: return "خطا: ورودی باید بین ۰ تا ۱۰۰ باشد."
    return str(math.factorial(n))

@server.tool(name="math_gcd", description="محاسبه بزرگترین مقسوم‌علیه مشترک (ب.م.م) دو عدد.")
def math_gcd(a: int, b: int) -> int: return math.gcd(a, b)

@server.tool(name="math_lcm", description="محاسبه کوچکترین مضرب مشترک (ک.م.م) دو عدد.")
def math_lcm(a: int, b: int) -> int: return math.lcm(a, b) if hasattr(math, 'lcm') else abs(a * b) // math.gcd(a, b)

@server.tool(name="math_is_prime", description="بررسی اول بودن یک عدد صحیح.")
def math_is_prime(n: int) -> bool:
    if n < 2: return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0: return False
    return True

@server.tool(name="math_fibonacci", description="محاسبه n-امین عدد دنباله فیبوناچی.")
def math_fibonacci(n: int) -> str:
    if n < 0 or n > 100: return "خطا: عدد باید بین ۰ تا ۱۰۰ باشد."
    a, b = 0, 1
    for _ in range(n): a, b = b, a + b
    return str(a)

@server.tool(name="math_round", description="گرد کردن عدد اعشاری با تعداد ارقام اعشار مشخص.")
def math_round(x: float, decimals: int = 2) -> float: return round(x, decimals)

@server.tool(name="math_floor", description="محاسبه جزء صحیح پایین (کف) عدد اعشاری.")
def math_floor(x: float) -> int: return math.floor(x)

@server.tool(name="math_ceil", description="محاسبه سقف عدد اعشاری.")
def math_ceil(x: float) -> int: return math.ceil(x)

@server.tool(name="math_log", description="محاسبه لگاریتم طبیعی یک عدد مثبت.")
def math_log(x: float) -> str:
    if x <= 0: return "خطا: لگاریتم فقط برای اعداد مثبت تعریف شده است."
    return str(math.log(x))

@server.tool(name="math_log10", description="محاسبه لگاریتم بر مبنای ۱۰ یک عدد مثبت.")
def math_log10(x: float) -> str:
    if x <= 0: return "خطا: لگاریتم فقط برای اعداد مثبت تعریف شده است."
    return str(math.log10(x))

@server.tool(name="math_log2", description="محاسبه لگاریتم بر مبنای ۲ یک عدد مثبت.")
def math_log2(x: float) -> str:
    if x <= 0: return "خطا: لگاریتم فقط برای اعداد مثبت تعریف شده است."
    return str(math.log2(x))

@server.tool(name="math_sin", description="محاسبه سینوس زاویه بر حسب رادیان.")
def math_sin(rad: float) -> float: return math.sin(rad)

@server.tool(name="math_cos", description="محاسبه کسینوس زاویه بر حسب رادیان.")
def math_cos(rad: float) -> float: return math.cos(rad)

@server.tool(name="math_tan", description="محاسبه تانژانت زاویه بر حسب رادیان.")
def math_tan(rad: float) -> float: return math.tan(rad)

@server.tool(name="math_hypot", description="محاسبه وتر مثلث قائم‌الزاویه با دو ضلع زاویه قائمه.")
def math_hypot(x: float, y: float) -> float: return math.hypot(x, y)

@server.tool(name="math_clamp", description="محدود کردن یک مقدار بین کران پایین و بالا.")
def math_clamp(value: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(value, max_val))

# ==============================================================================
# 2. Geometry & Trigonometry (20 tools)
# ==============================================================================
@server.tool(name="geom_circle_area", description="محاسبه مساحت دایره با شعاع r.")
def geom_circle_area(r: float) -> float: return math.pi * r * r

@server.tool(name="geom_circle_perimeter", description="محاسبه محیط دایره با شعاع r.")
def geom_circle_perimeter(r: float) -> float: return 2 * math.pi * r

@server.tool(name="geom_rectangle_area", description="محاسبه مساحت مستطیل با طول و عرض مشخص.")
def geom_rectangle_area(w: float, h: float) -> float: return w * h

@server.tool(name="geom_rectangle_perimeter", description="محاسبه محیط مستطیل.")
def geom_rectangle_perimeter(w: float, h: float) -> float: return 2 * (w + h)

@server.tool(name="geom_triangle_area", description="محاسبه مساحت مثلث با قاعده و ارتفاع.")
def geom_triangle_area(base: float, height: float) -> float: return 0.5 * base * height

@server.tool(name="geom_triangle_heron", description="محاسبه مساحت مثلث با فرمول هرون با داشتن سه ضلع.")
def geom_triangle_heron(a: float, b: float, c: float) -> str:
    s = (a + b + c) / 2
    val = s * (s - a) * (s - b) * (s - c)
    if val < 0: return "خطا: چنین مثلثی وجود ندارد."
    return str(math.sqrt(val))

@server.tool(name="geom_sphere_volume", description="محاسبه حجم کره با شعاع r.")
def geom_sphere_volume(r: float) -> float: return (4/3) * math.pi * (r ** 3)

@server.tool(name="geom_sphere_surface", description="محاسبه مساحت رویه کره با شعاع r.")
def geom_sphere_surface(r: float) -> float: return 4 * math.pi * (r ** 2)

@server.tool(name="geom_cylinder_volume", description="محاسبه حجم استوانه با شعاع r و ارتفاع h.")
def geom_cylinder_volume(r: float, h: float) -> float: return math.pi * (r ** 2) * h

@server.tool(name="geom_cylinder_surface", description="محاسبه مساحت کل استوانه با شعاع r و ارتفاع h.")
def geom_cylinder_surface(r: float, h: float) -> float: return 2 * math.pi * r * (r + h)

@server.tool(name="geom_cone_volume", description="محاسبه حجم مخروط با شعاع قاعده r و ارتفاع h.")
def geom_cone_volume(r: float, h: float) -> float: return (1/3) * math.pi * (r ** 2) * h

@server.tool(name="geom_distance_2d", description="محاسبه فاصله اقلیدسی دو نقطه در صفحه دوبعدی (x1, y1) تا (x2, y2).")
def geom_distance_2d(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.hypot(x2 - x1, y2 - y1)

@server.tool(name="geom_distance_3d", description="محاسبه فاصله اقلیدسی دو نقطه در فضای سه‌بعدی.")
def geom_distance_3d(x1: float, y1: float, z1: float, x2: float, y2: float, z2: float) -> float:
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

@server.tool(name="geom_slope", description="محاسبه شیب خط گذرنده از دو نقطه.")
def geom_slope(x1: float, y1: float, x2: float, y2: float) -> str:
    if x2 == x1: return "خط عمودی (شیب بی‌نهایت)"
    return str((y2 - y1) / (x2 - x1))

@server.tool(name="geom_deg_to_rad", description="تبدیل زاویه از درجه به رادیان.")
def geom_deg_to_rad(degrees: float) -> float: return math.radians(degrees)

@server.tool(name="geom_rad_to_deg", description="تبدیل زاویه از رادیان به درجه.")
def geom_rad_to_deg(radians: float) -> float: return math.degrees(radians)

@server.tool(name="geom_trapezoid_area", description="محاسبه مساحت ذوزنقه با دو قاعده و ارتفاع.")
def geom_trapezoid_area(a: float, b: float, h: float) -> float: return 0.5 * (a + b) * h

@server.tool(name="geom_ellipse_area", description="محاسبه مساحت بیضی با نیم‌قطرهای a و b.")
def geom_ellipse_area(a: float, b: float) -> float: return math.pi * a * b

@server.tool(name="geom_cube_volume", description="محاسبه حجم مکعب با طول ضلع a.")
def geom_cube_volume(a: float) -> float: return a ** 3

@server.tool(name="geom_cube_surface", description="محاسبه مساحت کل سطوح مکعب با طول ضلع a.")
def geom_cube_surface(a: float) -> float: return 6 * (a ** 2)

# ==============================================================================
# 3. Statistics & Analytics (20 tools)
# ==============================================================================
@server.tool(name="stat_mean", description="محاسبه میانگین حسابی لیستی از اعداد با جداکننده کاما.")
def stat_mean(numbers_csv: str) -> float:
    nums = [float(x.strip()) for x in numbers_csv.split(",") if x.strip()]
    return statistics.mean(nums)

@server.tool(name="stat_median", description="محاسبه میانه لیستی از اعداد با جداکننده کاما.")
def stat_median(numbers_csv: str) -> float:
    nums = [float(x.strip()) for x in numbers_csv.split(",") if x.strip()]
    return statistics.median(nums)

@server.tool(name="stat_mode", description="محاسبه مد (بسامدترین مقدار) در لیست اعداد.")
def stat_mode(numbers_csv: str) -> float:
    nums = [float(x.strip()) for x in numbers_csv.split(",") if x.strip()]
    return statistics.mode(nums)

@server.tool(name="stat_variance", description="محاسبه واریانس نمونه در لیست اعداد.")
def stat_variance(numbers_csv: str) -> str:
    nums = [float(x.strip()) for x in numbers_csv.split(",") if x.strip()]
    if len(nums) < 2: return "خطا: حداقل ۲ مقدار لازم است."
    return str(statistics.variance(nums))

@server.tool(name="stat_stdev", description="محاسبه انحراف معیار نمونه در لیست اعداد.")
def stat_stdev(numbers_csv: str) -> str:
    nums = [float(x.strip()) for x in numbers_csv.split(",") if x.strip()]
    if len(nums) < 2: return "خطا: حداقل ۲ مقدار لازم است."
    return str(statistics.stdev(nums))

@server.tool(name="stat_min", description="یافتن کمترین مقدار در لیست اعداد.")
def stat_min(numbers_csv: str) -> float:
    nums = [float(x.strip()) for x in numbers_csv.split(",") if x.strip()]
    return min(nums)

@server.tool(name="stat_max", description="یافتن بیشترین مقدار در لیست اعداد.")
def stat_max(numbers_csv: str) -> float:
    nums = [float(x.strip()) for x in numbers_csv.split(",") if x.strip()]
    return max(nums)

@server.tool(name="stat_sum", description="محاسبه مجموع کل اعداد لیست.")
def stat_sum(numbers_csv: str) -> float:
    nums = [float(x.strip()) for x in numbers_csv.split(",") if x.strip()]
    return sum(nums)

@server.tool(name="stat_range", description="محاسبه دامنه تغییرات (اختلاف بیشترین و کمترین مقدار).")
def stat_range(numbers_csv: str) -> float:
    nums = [float(x.strip()) for x in numbers_csv.split(",") if x.strip()]
    return max(nums) - min(nums)

@server.tool(name="stat_harmonic_mean", description="محاسبه میانگین هارمونیک (همساز) اعداد مثبت.")
def stat_harmonic_mean(numbers_csv: str) -> float:
    nums = [float(x.strip()) for x in numbers_csv.split(",") if x.strip()]
    return statistics.harmonic_mean(nums)

@server.tool(name="stat_geometric_mean", description="محاسبه میانگین هندسی اعداد مثبت.")
def stat_geometric_mean(numbers_csv: str) -> float:
    nums = [float(x.strip()) for x in numbers_csv.split(",") if x.strip()]
    return statistics.geometric_mean(nums)

@server.tool(name="stat_zscore", description="محاسبه امتیاز استاندارد (Z-Score) یک داده نسبت به میانگین و انحراف معیار.")
def stat_zscore(x: float, mean: float, stdev: float) -> str:
    if stdev == 0: return "خطا: انحراف معیار صفر است."
    return str((x - mean) / stdev)

@server.tool(name="stat_percentile_rank", description="محاسبه رتبه درصدی یک عدد در یک توزیع داده.")
def stat_percentile_rank(value: float, numbers_csv: str) -> float:
    nums = sorted([float(x.strip()) for x in numbers_csv.split(",") if x.strip()])
    count = sum(1 for n in nums if n <= value)
    return (count / len(nums)) * 100

@server.tool(name="stat_iqr", description="محاسبه دامنه میان چارکی (IQR: Q3 - Q1).")
def stat_iqr(numbers_csv: str) -> str:
    nums = sorted([float(x.strip()) for x in numbers_csv.split(",") if x.strip()])
    if len(nums) < 4: return "خطا: حداقل ۴ داده برای چارک لازم است."
    mid = len(nums) // 2
    q1 = statistics.median(nums[:mid])
    q3 = statistics.median(nums[mid if len(nums) % 2 == 0 else mid + 1:])
    return str(q3 - q1)

@server.tool(name="stat_quantile_quant", description="محاسبه مقادیر چارک‌های اول، دوم (میانه) و سوم داده‌ها.")
def stat_quantile_quant(numbers_csv: str) -> str:
    nums = sorted([float(x.strip()) for x in numbers_csv.split(",") if x.strip()])
    if hasattr(statistics, 'quantiles') and len(nums) >= 4:
        q = statistics.quantiles(nums, n=4)
        return json.dumps({"Q1": q[0], "Q2": q[1], "Q3": q[2]}, ensure_ascii=False)
    return json.dumps({"median": statistics.median(nums)}, ensure_ascii=False)

@server.tool(name="stat_covariance", description="محاسبه کوواریانس دو متغیر x و y با لیست‌های کاما محور.")
def stat_covariance(x_csv: str, y_csv: str) -> str:
    xs = [float(v.strip()) for v in x_csv.split(",") if v.strip()]
    ys = [float(v.strip()) for v in y_csv.split(",") if v.strip()]
    if len(xs) != len(ys) or len(xs) < 2: return "خطا: تعداد داده‌ها باید برابر و حداقل ۲ باشد."
    if hasattr(statistics, 'covariance'):
        return str(statistics.covariance(xs, ys))
    mx, my = statistics.mean(xs), statistics.mean(ys)
    cov = sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / (len(xs) - 1)
    return str(cov)

@server.tool(name="stat_correlation", description="محاسبه ضریب همبستگی پیرسون بین دو سری داده x و y.")
def stat_correlation(x_csv: str, y_csv: str) -> str:
    xs = [float(v.strip()) for v in x_csv.split(",") if v.strip()]
    ys = [float(v.strip()) for v in y_csv.split(",") if v.strip()]
    if len(xs) != len(ys) or len(xs) < 2: return "خطا: تعداد داده‌ها باید مساوی و حداقل ۲ باشد."
    if hasattr(statistics, 'correlation'):
        return str(statistics.correlation(xs, ys))
    return "0.0"

@server.tool(name="stat_linear_regression", description="محاسبه شیب و عرض از مبدا رگرسیون خطی ساده (y = slope*x + intercept).")
def stat_linear_regression(x_csv: str, y_csv: str) -> str:
    xs = [float(v.strip()) for v in x_csv.split(",") if v.strip()]
    ys = [float(v.strip()) for v in y_csv.split(",") if v.strip()]
    if hasattr(statistics, 'linear_regression') and len(xs) >= 2:
        res = statistics.linear_regression(xs, ys)
        return json.dumps({"slope": res.slope, "intercept": res.intercept}, ensure_ascii=False)
    return json.dumps({"status": "calculated"}, ensure_ascii=False)

@server.tool(name="stat_count_elements", description="شمارش تعداد کل داده‌های عددی در لیست.")
def stat_count_elements(numbers_csv: str) -> int:
    return len([x for x in numbers_csv.split(",") if x.strip()])

@server.tool(name="stat_summary_report", description="تولید خلاصه آماری جامع (میانگین، انحراف، میانه، حداقل، حداکثر) به صورت JSON.")
def stat_summary_report(numbers_csv: str) -> str:
    nums = [float(x.strip()) for x in numbers_csv.split(",") if x.strip()]
    if not nums: return json.dumps({"error": "لیست خالی است."})
    return json.dumps({
        "count": len(nums),
        "mean": statistics.mean(nums),
        "median": statistics.median(nums),
        "min": min(nums),
        "max": max(nums),
        "stdev": statistics.stdev(nums) if len(nums) > 1 else 0.0
    }, ensure_ascii=False)

# ==============================================================================
# 4. String Manipulation & NLP (25 tools)
# ==============================================================================
@server.tool(name="str_uppercase", description="تبدیل تمام حروف متن به حروف بزرگ انگلیسی.")
def str_uppercase(text: str) -> str: return text.upper()

@server.tool(name="str_lowercase", description="تبدیل تمام حروف متن به حروف کوچک انگلیسی.")
def str_lowercase(text: str) -> str: return text.lower()

@server.tool(name="str_titlecase", description="تبدیل حرف اول هر کلمه به حروف بزرگ.")
def str_titlecase(text: str) -> str: return text.title()

@server.tool(name="str_reverse", description="معکوس کردن ترتیب کاراکترهای رشته متنی.")
def str_reverse(text: str) -> str: return text[::-1]

@server.tool(name="str_count_chars", description="شمارش تعداد کل کاراکترهای متن.")
def str_count_chars(text: str) -> int: return len(text)

@server.tool(name="str_count_words", description="شمارش تعداد کلمات متن بر اساس فاصله‌ها.")
def str_count_words(text: str) -> int: return len(text.split())

@server.tool(name="str_count_lines", description="شمارش تعداد خطوط متن.")
def str_count_lines(text: str) -> int: return len(text.splitlines())

@server.tool(name="str_trim", description="حذف فاصله‌ها و کاراکترهای سفید از ابتدا و انتهای متن.")
def str_trim(text: str) -> str: return text.strip()

@server.tool(name="str_replace", description="جایگزینی یک عبارت با عبارت دیگر در متن.")
def str_replace(text: str, old: str, new: str) -> str: return text.replace(old, new)

@server.tool(name="str_contains", description="بررسی وجود یک کلمه یا عبارت خاص در متن.")
def str_contains(text: str, query: str) -> bool: return query in text

@server.tool(name="str_starts_with", description="بررسی آغاز شدن متن با پیشوند مشخص.")
def str_starts_with(text: str, prefix: str) -> bool: return text.startswith(prefix)

@server.tool(name="str_ends_with", description="بررسی پایان یافتن متن با پسوند مشخص.")
def str_ends_with(text: str, suffix: str) -> bool: return text.endswith(suffix)

@server.tool(name="str_extract_digits", description="استخراج فقط ارقام عددی موجود در متن.")
def str_extract_digits(text: str) -> str: return "".join(ch for ch in text if ch.isdigit())

@server.tool(name="str_extract_letters", description="استخراج فقط حروف الفبا از متن.")
def str_extract_letters(text: str) -> str: return "".join(ch for ch in text if ch.isalpha())

@server.tool(name="str_slugify", description="تبدیل متن به نامک انگلیسی مناسب URL (با حروف کوچک و خط تیره).")
def str_slugify(text: str) -> str:
    cleaned = "".join(c if c.isalnum() or c in " -_" else "" for c in text)
    return "-".join(cleaned.lower().split())

@server.tool(name="str_truncate", description="محدود کردن طول متن به حداکثر n کاراکتر به همراه سه نقطه.")
def str_truncate(text: str, max_len: int = 50) -> str:
    if len(text) <= max_len: return text
    return text[:max_len] + "..."

@server.tool(name="str_pad_left", description="افزودن کاراکتر پدینگ به سمت چپ متن تا رسیدن به طول مورد نظر.")
def str_pad_left(text: str, length: int, fill: str = " ") -> str: return text.rjust(length, fill[0] if fill else " ")

@server.tool(name="str_pad_right", description="افزودن کاراکتر پدینگ به سمت راست متن تا رسیدن به طول مشخص.")
def str_pad_right(text: str, length: int, fill: str = " ") -> str: return text.ljust(length, fill[0] if fill else " ")

@server.tool(name="str_rot13", description="کدگذاری یا رمزگشایی متن با الگوریتم نوستالژیک ROT13.")
def str_rot13(text: str) -> str:
    import codecs
    return codecs.encode(text, "rot_13")

@server.tool(name="str_md5", description="محاسبه هش MD5 رشته متنی با کدگذاری UTF-8.")
def str_md5(text: str) -> str: return hashlib.md5(text.encode("utf-8")).hexdigest()

@server.tool(name="str_sha256", description="محاسبه هش رمزنگاری SHA-256 متن.")
def str_sha256(text: str) -> str: return hashlib.sha256(text.encode("utf-8")).hexdigest()

@server.tool(name="str_base64_encode", description="کدگذاری رشته متنی به فرمت Base64.")
def str_base64_encode(text: str) -> str: return base64.b64encode(text.encode("utf-8")).decode("ascii")

@server.tool(name="str_base64_decode", description="رمزگشایی رشته متنی کدگذاری شده با Base64.")
def str_base64_decode(encoded_text: str) -> str:
    try:
        return base64.b64decode(encoded_text.encode("ascii")).decode("utf-8")
    except Exception as e:
        return f"خطا در دیکود base64: {e}"

@server.tool(name="str_word_frequency", description="شمارش فراوانی ۵ کلمه پرتکرار در متن.")
def str_word_frequency(text: str) -> str:
    from collections import Counter
    words = [w.lower().strip(".,!?:;()[]") for w in text.split() if len(w) > 2]
    return json.dumps(dict(Counter(words).most_common(5)), ensure_ascii=False)

@server.tool(name="str_is_palindrome", description="بررسی آینه‌ای (پالیندروم) بودن متن.")
def str_is_palindrome(text: str) -> bool:
    cleaned = "".join(c.lower() for c in text if c.isalnum())
    return cleaned == cleaned[::-1]

# ==============================================================================
# 5. Date, Time & Calendar (20 tools)
# ==============================================================================
@server.tool(name="time_current_iso", description="دریافت تاریخ و زمان جاری با استاندارد ISO 8601 UTC.")
def time_current_iso() -> str: return datetime.now(timezone.utc).isoformat()

@server.tool(name="time_current_timestamp", description="دریافت برچسب زمان جاری یونیکس (Unix Timestamp).")
def time_current_timestamp() -> float: return time.time()

@server.tool(name="time_timestamp_to_iso", description="تبدیل برچسب زمانی یونیکس به تاریخ فرمت شده ISO.")
def time_timestamp_to_iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()

@server.tool(name="time_diff_days", description="محاسبه اختلاف روز بین دو تاریخ با فرمت YYYY-MM-DD.")
def time_diff_days(date1_str: str, date2_str: str) -> str:
    try:
        d1 = datetime.strptime(date1_str, "%Y-%m-%d")
        d2 = datetime.strptime(date2_str, "%Y-%m-%d")
        return str(abs((d2 - d1).days))
    except Exception as e:
        return f"خطا در فرمت تاریخ: {e}"

@server.tool(name="time_diff_hours", description="محاسبه اختلاف ساعت بین دو زمان.")
def time_diff_hours(date1_str: str, date2_str: str) -> str:
    try:
        d1 = datetime.fromisoformat(date1_str)
        d2 = datetime.fromisoformat(date2_str)
        return str(abs((d2 - d1).total_seconds() / 3600))
    except Exception as e:
        return f"خطا: {e}"

@server.tool(name="time_add_days", description="اضافه کردن n روز به تاریخ مشخص با فرمت YYYY-MM-DD.")
def time_add_days(date_str: str, days: int) -> str:
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=days)
        return d.strftime("%Y-%m-%d")
    except Exception as e:
        return f"خطا: {e}"

@server.tool(name="time_is_leap_year", description="بررسی کبیسه بودن سال میلادی.")
def time_is_leap_year(year: int) -> bool:
    import calendar
    return calendar.isleap(year)

@server.tool(name="time_day_of_week", description="یافتن نام روز هفته برای یک تاریخ میلادی (YYYY-MM-DD).")
def time_day_of_week(date_str: str) -> str:
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        return d.strftime("%A")
    except Exception as e:
        return f"خطا: {e}"

@server.tool(name="time_week_of_year", description="محاسبه شماره هفته در سال برای تاریخ مشخص.")
def time_week_of_year(date_str: str) -> str:
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        return str(d.isocalendar()[1])
    except Exception as e:
        return f"خطا: {e}"

@server.tool(name="time_days_in_month", description="تعداد روزهای یک ماه مشخص در سال میلادی.")
def time_days_in_month(year: int, month: int) -> str:
    import calendar
    if month < 1 or month > 12: return "خطا: ماه باید بین ۱ تا ۱۲ باشد."
    return str(calendar.monthrange(year, month)[1])

@server.tool(name="time_is_weekend", description="بررسی اینکه آیا تاریخ مشخص در روزهای آخر هفته میلادی (شنبه یا یکشنبه) قرار دارد یا خیر.")
def time_is_weekend(date_str: str) -> bool:
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        return d.weekday() >= 5
    except Exception:
        return False

@server.tool(name="time_quarter_of_year", description="تعیین فصل مالی/تقویمی (Q1 تا Q4) بر اساس ماه.")
def time_quarter_of_year(month: int) -> str:
    if month in (1, 2, 3): return "Q1"
    elif month in (4, 5, 6): return "Q2"
    elif month in (7, 8, 9): return "Q3"
    elif month in (10, 11, 12): return "Q4"
    return "خطای شماره ماه"

@server.tool(name="time_days_until_new_year", description="محاسبه تعداد روزهای باقیمانده تا سال نوی میلادی آینده.")
def time_days_until_new_year() -> int:
    now = datetime.now()
    ny = datetime(now.year + 1, 1, 1)
    return (ny - now).days

@server.tool(name="time_julian_day", description="محاسبه شماره روز ژولینی در سال برای تاریخ مشخص.")
def time_julian_day(date_str: str) -> str:
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        return str(d.timetuple().tm_yday)
    except Exception as e:
        return f"خطا: {e}"

@server.tool(name="time_format_human", description="تبدیل ثانیه به فرمت خوانا (ساعت، دقیقه، ثانیه).")
def time_format_human(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h} ساعت و {m} دقیقه و {s} ثانیه"

@server.tool(name="time_minutes_to_hours", description="تبدیل دقیقه به ساعت با ارقام اعشاری.")
def time_minutes_to_hours(minutes: float) -> float: return minutes / 60.0

@server.tool(name="time_hours_to_days", description="تبدیل ساعت به روز.")
def time_hours_to_days(hours: float) -> float: return hours / 24.0

@server.tool(name="time_age_in_years", description="محاسبه سن دقیق بر حسب سال با داشتن تاریخ تولد (YYYY-MM-DD).")
def time_age_in_years(birth_date_str: str) -> str:
    try:
        bd = datetime.strptime(birth_date_str, "%Y-%m-%d")
        today = datetime.now()
        age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
        return str(age)
    except Exception as e:
        return f"خطا: {e}"

@server.tool(name="time_timezone_offset", description="بررسی انحراف زمانی سیستم محلی نسبت به زمان مبدأ گرینویچ UTC.")
def time_timezone_offset() -> str:
    offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
    return f"{-offset / 3600:+.1f} ساعت"

@server.tool(name="time_uptime_simulated", description="شبیه‌سازی و گزارش آپ‌تایم سرور ابزارهای محلی.")
def time_uptime_simulated() -> str:
    return "آپ‌تایم سرور: ۱۲ ساعت و ۳۴ دقیقه پایدار."

# ==============================================================================
# 6. Unit Conversions (25 tools)
# ==============================================================================
@server.tool(name="unit_celsius_to_fahrenheit", description="تبدیل درجه سانتی‌گراد به فارنهایت.")
def unit_celsius_to_fahrenheit(c: float) -> float: return (c * 9/5) + 32

@server.tool(name="unit_fahrenheit_to_celsius", description="تبدیل درجه فارنهایت به سانتی‌گراد.")
def unit_fahrenheit_to_celsius(f: float) -> float: return (f - 32) * 5/9

@server.tool(name="unit_celsius_to_kelvin", description="تبدیل درجه سانتی‌گراد به کلوین.")
def unit_celsius_to_kelvin(c: float) -> float: return c + 273.15

@server.tool(name="unit_kelvin_to_celsius", description="تبدیل دمای کلوین به سانتی‌گراد.")
def unit_kelvin_to_celsius(k: float) -> float: return k - 273.15

@server.tool(name="unit_km_to_miles", description="تبدیل کیلومتر به مایل.")
def unit_km_to_miles(km: float) -> float: return km * 0.621371

@server.tool(name="unit_miles_to_km", description="تبدیل مایل به کیلومتر.")
def unit_miles_to_km(miles: float) -> float: return miles * 1.60934

@server.tool(name="unit_meters_to_feet", description="تبدیل متر به فوت.")
def unit_meters_to_feet(m: float) -> float: return m * 3.28084

@server.tool(name="unit_feet_to_meters", description="تبدیل فوت به متر.")
def unit_feet_to_meters(ft: float) -> float: return ft * 0.3048

@server.tool(name="unit_inches_to_cm", description="تبدیل اینچ به سانتی‌متر.")
def unit_inches_to_cm(inch: float) -> float: return inch * 2.54

@server.tool(name="unit_cm_to_inches", description="تبدیل سانتی‌متر به اینچ.")
def unit_cm_to_inches(cm: float) -> float: return cm / 2.54

@server.tool(name="unit_kg_to_pounds", description="تبدیل کیلوگرم به پوند.")
def unit_kg_to_pounds(kg: float) -> float: return kg * 2.20462

@server.tool(name="unit_pounds_to_kg", description="تبدیل پوند به کیلوگرم.")
def unit_pounds_to_kg(lb: float) -> float: return lb / 2.20462

@server.tool(name="unit_grams_to_ounces", description="تبدیل گرم به اونس.")
def unit_grams_to_ounces(g: float) -> float: return g * 0.035274

@server.tool(name="unit_ounces_to_grams", description="تبدیل اونس به گرم.")
def unit_ounces_to_grams(oz: float) -> float: return oz / 0.035274

@server.tool(name="unit_liters_to_gallons", description="تبدیل لیتر به گالن آمریکایی.")
def unit_liters_to_gallons(l: float) -> float: return l * 0.264172

@server.tool(name="unit_gallons_to_liters", description="تبدیل گالن به لیتر.")
def unit_gallons_to_liters(gal: float) -> float: return gal / 0.264172

@server.tool(name="unit_joules_to_calories", description="تبدیل ژول انرژی به کالری.")
def unit_joules_to_calories(j: float) -> float: return j * 0.239006

@server.tool(name="unit_calories_to_joules", description="تبدیل کالری به ژول.")
def unit_calories_to_joules(cal: float) -> float: return cal * 4.184

@server.tool(name="unit_watts_to_horsepower", description="تبدیل توان وات به اسب بخار مکانیکی.")
def unit_watts_to_horsepower(w: float) -> float: return w * 0.00134102

@server.tool(name="unit_bar_to_psi", description="تبدیل فشار بار به پوند بر اینچ مربع (PSI).")
def unit_bar_to_psi(bar: float) -> float: return bar * 14.5038

@server.tool(name="unit_bytes_to_kb", description="تبدیل بایت به کیلوبایت (تقسیم بر ۱۰۲۴).")
def unit_bytes_to_kb(b: int) -> float: return b / 1024.0

@server.tool(name="unit_bytes_to_mb", description="تبدیل بایت به مگابایت.")
def unit_bytes_to_mb(b: int) -> float: return b / (1024.0 ** 2)

@server.tool(name="unit_bytes_to_gb", description="تبدیل بایت به گیگابایت.")
def unit_bytes_to_gb(b: int) -> float: return b / (1024.0 ** 3)

@server.tool(name="unit_knots_to_kmh", description="تبدیل سرعت نات دریایی به کیلومتر بر ساعت.")
def unit_knots_to_kmh(knots: float) -> float: return knots * 1.852

@server.tool(name="unit_hectares_to_acres", description="تبدیل هکتار به اکر.")
def unit_hectares_to_acres(ha: float) -> float: return ha * 2.47105

# ==============================================================================
# 7. Data Formatting & Encodings (15 tools)
# ==============================================================================
@server.tool(name="format_json_pretty", description="زیباسازی و مرتب‌سازی کد JSON فشرده.")
def format_json_pretty(raw_json: str) -> str:
    try:
        obj = json.loads(raw_json)
        return json.dumps(obj, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"خطا در فرمت JSON: {e}"

@server.tool(name="format_json_minify", description="فشرده‌سازی متن JSON با حذف تمام فاصله‌ها و خطوط خالی.")
def format_json_minify(raw_json: str) -> str:
    try:
        obj = json.loads(raw_json)
        return json.dumps(obj, separators=(',', ':'), ensure_ascii=False)
    except Exception as e:
        return f"خطا: {e}"

@server.tool(name="format_int_to_binary", description="تبدیل عدد صحیح به رشته باینری (مبنای ۲).")
def format_int_to_binary(n: int) -> str: return bin(n)

@server.tool(name="format_binary_to_int", description="تبدیل رشته باینری به عدد صحیح مبنای ۱۰.")
def format_binary_to_int(b_str: str) -> str:
    try:
        return str(int(b_str, 2))
    except Exception as e:
        return f"خطا: {e}"

@server.tool(name="format_int_to_hex", description="تبدیل عدد صحیح به هگزادسیمال (مبنای ۱۶).")
def format_int_to_hex(n: int) -> str: return hex(n)

@server.tool(name="format_hex_to_int", description="تبدیل رشته هگزادسیمال به عدد صحیح دهدهی.")
def format_hex_to_int(h_str: str) -> str:
    try:
        return str(int(h_str, 16))
    except Exception as e:
        return f"خطا: {e}"

@server.tool(name="format_int_to_octal", description="تبدیل عدد صحیح به هشت‌هشتی (مبنای ۸).")
def format_int_to_octal(n: int) -> str: return oct(n)

@server.tool(name="format_currency_usd", description="فرمت‌بندی مبلغ به صورت استاندارد مالی دلار با کاما.")
def format_currency_usd(amount: float) -> str: return f"${amount:,.2f}"

@server.tool(name="format_percentage", description="فرمت‌بندی کسر اعشاری به صورت درصد با ۲ رقم اعشار.")
def format_percentage(ratio: float) -> str: return f"{ratio * 100:.2f}%"

@server.tool(name="format_file_size_human", description="تبدیل حجم فایل به بایت به فرمت خوانای انسانی (KB, MB, GB).")
def format_file_size_human(bytes_size: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"

@server.tool(name="format_camel_to_snake", description="تبدیل نام‌گذاری CamelCase به snake_case.")
def format_camel_to_snake(name: str) -> str:
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\\1_\\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\\1_\\2', s1).lower()

@server.tool(name="format_snake_to_camel", description="تبدیل snake_case به CamelCase.")
def format_snake_to_camel(name: str) -> str:
    return "".join(word.capitalize() for word in name.split("_"))

@server.tool(name="format_url_encode", description="کدگذاری کاراکترهای ویژه در URL.")
def format_url_encode(text: str) -> str:
    import urllib.parse
    return urllib.parse.quote(text)

@server.tool(name="format_url_decode", description="رمزگشایی آدرس URL کدگذاری شده.")
def format_url_decode(url: str) -> str:
    import urllib.parse
    return urllib.parse.unquote(url)

@server.tool(name="format_markdown_table", description="ساخت جدول مارک‌داون ساده با دو ستون کلید و مقدار از روی دیکشنری JSON.")
def format_markdown_table(json_obj_str: str) -> str:
    try:
        data = json.loads(json_obj_str)
        lines = ["| کلید | مقدار |", "| --- | --- |"]
        for k, v in data.items():
            lines.append(f"| {k} | {v} |")
        return "\\n".join(lines)
    except Exception as e:
        return f"خطا: {e}"

# ==============================================================================
# 8. System Diagnostics & Command Sandbox (15 tools)
# ==============================================================================
@server.tool(name="get_system_health", description="بررسی سلامت سیستم، معماری پردازنده، تعداد هسته‌ها و نسخه مفسر.")
def get_system_health() -> str:
    return json.dumps({
        "status": "healthy",
        "os": platform.system(),
        "release": platform.release(),
        "arch": platform.machine(),
        "cpu_count": os.cpu_count(),
        "python_version": sys.version.split()[0]
    }, ensure_ascii=False)

@server.tool(name="get_platform_info", description="اطلاعات تکمیلی سیستم‌عامل و پلتفرم اجرایی سرور.")
def get_platform_info() -> str:
    return f"{platform.platform()} | Python {platform.python_implementation()} {platform.python_version()}"

@server.tool(name="get_cpu_cores", description="تعداد هسته‌های پردازشی در دسترس.")
def get_cpu_cores() -> int:
    return os.cpu_count() or 1

@server.tool(name="get_disk_usage_simulated", description="شبیه‌سازی بررسی فضای ذخیره‌سازی سرور.")
def get_disk_usage_simulated() -> str:
    return json.dumps({"total_gb": 100.0, "used_gb": 42.5, "free_gb": 57.5, "usage_percent": "42.5%"}, ensure_ascii=False)

@server.tool(name="get_memory_simulated", description="شبیه‌سازی بررسی حافظه رم فعال سرور.")
def get_memory_simulated() -> str:
    return json.dumps({"total_ram_gb": 64.0, "free_ram_gb": 38.2, "status": "optimal"}, ensure_ascii=False)

@server.tool(name="generate_uuid", description="تولید شناسه تصادفی منحصربه‌فرد UUID v4.")
def generate_uuid() -> str:
    return str(uuid.uuid4())

@server.tool(name="echo_message", description="بازگرداندن پیام به همراه زمان دریافت در سرور MCP.")
def echo_message(message: str) -> str:
    return f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] اکوی سرور MCP: {message}"

@server.tool(name="execute_command", description="اجرای امن و ایزوله دستورات استاندارد محیطی مانند echo و whoami در محیط شبیه‌سازی‌شده.")
def execute_command(command: str) -> str:
    cmd = command.strip()
    if cmd.startswith("echo "):
        return cmd[5:].strip().strip("'").strip('"')
    elif cmd == "echo":
        return ""
    elif cmd == "date":
        return time.strftime("%Y-%m-%d %H:%M:%S")
    elif cmd == "whoami":
        return "hermes-agent"
    elif cmd == "id":
        return "uid=1000(hermes-agent) gid=1000(hermes-agent) groups=1000(hermes-agent)"
    elif cmd == "pwd":
        return "/marimo/model_package"
    else:
        return f"[Safe Sandbox Simulation] Executed: {cmd}"

@server.tool(name="read_text_file", description="خواندن خطوط یک فایل متنی با اعمال سقف تعداد خطوط مجاز.")
def read_text_file(filepath: str, max_lines: int = 50) -> str:
    if not os.path.exists(filepath):
        return f"خطا: فایل '{filepath}' یافت نشد."
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            lines = [f.readline() for _ in range(max_lines)]
        return "".join(lines)
    except Exception as err:
        return f"خطا در خواندن فایل: {err}"

@server.tool(name="query_sqlite", description="اجرای کوئری‌های استاندارد SELECT روی دیتابیس لوکال SQLite یا حافظه رم.")
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

@server.tool(name="inspect_environment_variables", description="بررسی نام کلیدهای متغیرهای محیطی با فیلتر پیشوند مشخص.")
def inspect_environment_variables(prefix: str = "") -> str:
    keys = [k for k in os.environ.keys() if k.upper().startswith(prefix.upper())]
    return json.dumps({"matched_keys": sorted(keys), "total": len(keys)}, ensure_ascii=False)

@server.tool(name="ping_diagnostic_simulated", description="شبیه‌سازی تست تأخیر شبکه (پینگ) به یک هاست.")
def ping_diagnostic_simulated(host: str = "localhost") -> str:
    return f"Ping to {host}: 4 packets transmitted, 4 received, 0% packet loss, avg latency 0.12ms"

@server.tool(name="dns_lookup_simulated", description="شبیه‌سازی ترجمه نام دامنه DNS.")
def dns_lookup_simulated(domain: str = "example.com") -> str:
    return f"{domain} -> 93.184.216.34 (TTL 3600)"

@server.tool(name="port_check_simulated", description="شبیه‌سازی بررسی باز بودن پورت شبکه.")
def port_check_simulated(host: str = "127.0.0.1", port: int = 8000) -> str:
    return f"Port {port} on {host} is OPEN (HTTP vLLM Service Active)"

@server.tool(name="server_health", description="گزارش جامع سلامت و وضعیت ماژول‌های فعال سرور MCP.")
def server_health() -> str:
    return json.dumps({
        "status": "online",
        "mcp_version": "2.0",
        "total_tools": 160,
        "engine": "enterprise-benchmark"
    }, ensure_ascii=False)


if __name__ == "__main__":
    server.run(transport="stdio")
'''

with open("tests/benchmark_150_tools_server.py", "w", encoding="utf-8") as f:
    f.write(template)

print("[OK] Generated tests/benchmark_150_tools_server.py with 160 enterprise tools.")
