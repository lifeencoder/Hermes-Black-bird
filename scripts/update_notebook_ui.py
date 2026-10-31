from pathlib import Path

notebook_path = Path(r"c:\Users\farha\.gemini\antigravity\scratch\Hermes-Black-bird\notebook.py")
content = notebook_path.read_text(encoding="utf-8").replace("\r\n", "\n")

old_snippet = """    _shadow_js = \"\"\"(function() {
        function syncThemeAttrs(theme) {
            document.documentElement.setAttribute('data-theme', theme);
            if (document.body) {
                document.body.setAttribute('data-theme', theme);
                if (theme === 'dark') {
                    document.body.classList.remove('light', 'light-theme');
                    document.body.classList.add('dark', 'dark-theme');
                } else {
                    document.body.classList.remove('dark', 'dark-theme');
                    document.body.classList.add('light', 'light-theme');
                }
            }
        }

        var rootTheme = localStorage.getItem('hermes-theme') || 'dark';
        syncThemeAttrs(rootTheme);

        window.setHermesTheme = function(theme) {
            syncThemeAttrs(theme);
            localStorage.setItem('hermes-theme', theme);
            var iconEl = document.getElementById('theme-btn-icon');
            var textEl = document.getElementById('theme-btn-text');
            if (iconEl && textEl) {
                if (theme === 'dark') {
                    iconEl.textContent = '☀️';
                    textEl.textContent = 'حالت روشن';
                } else {
                    iconEl.textContent = '🌙';
                    textEl.textContent = 'حالت تاریک';
                }
            }
            updateAllShadows();
        };

        window.toggleHermesTheme = function() {
            var cur = document.documentElement.getAttribute('data-theme') || 'dark';
            window.setHermesTheme(cur === 'dark' ? 'light' : 'dark');
        };

        function updateAllShadows() {
            var curTheme = document.documentElement.getAttribute('data-theme') || 'dark';
            syncThemeAttrs(curTheme);
            var isDark = curTheme === 'dark';"""

new_snippet = """    _shadow_js = \"\"\"(function() {
        function syncThemeAttrs(theme) {
            document.documentElement.setAttribute('data-theme', theme);
            if (document.body) {
                document.body.setAttribute('data-theme', theme);
                if (theme === 'dark') {
                    document.body.classList.remove('light', 'light-theme');
                    document.body.classList.add('dark', 'dark-theme');
                } else {
                    document.body.classList.remove('dark', 'dark-theme');
                    document.body.classList.add('light', 'light-theme');
                }
            }
        }

        var rootTheme = localStorage.getItem('hermes-theme') || 'dark';
        syncThemeAttrs(rootTheme);

        window.setHermesTheme = function(theme) {
            syncThemeAttrs(theme);
            localStorage.setItem('hermes-theme', theme);
            var iconEl = document.getElementById('theme-btn-icon');
            var textEl = document.getElementById('theme-btn-text');
            if (iconEl && textEl) {
                if (theme === 'dark') {
                    iconEl.textContent = '☀️';
                    textEl.textContent = 'حالت روشن';
                } else {
                    iconEl.textContent = '🌙';
                    textEl.textContent = 'حالت تاریک';
                }
            }
            updateAllShadows();
        };

        window.toggleHermesTheme = function() {
            var cur = document.documentElement.getAttribute('data-theme') || 'dark';
            window.setHermesTheme(cur === 'dark' ? 'light' : 'dark');
        };

        // Delegated click listener to bypass Marimo HTML attribute sanitization
        if (!window._hermesThemeListenerAttached) {
            window._hermesThemeListenerAttached = true;
            document.addEventListener('click', function(e) {
                var btn = e.target && e.target.closest ? e.target.closest('#hermes-theme-toggle') : null;
                if (btn) {
                    e.preventDefault();
                    e.stopPropagation();
                    window.toggleHermesTheme();
                }
            });
        }

        function updateAllShadows() {
            var curTheme = document.documentElement.getAttribute('data-theme') || 'dark';
            syncThemeAttrs(curTheme);
            var isDark = curTheme === 'dark';

            var iconEl = document.getElementById('theme-btn-icon');
            var textEl = document.getElementById('theme-btn-text');
            if (iconEl && textEl) {
                if (isDark) {
                    iconEl.textContent = '☀️';
                    textEl.textContent = 'حالت روشن';
                } else {
                    iconEl.textContent = '🌙';
                    textEl.textContent = 'حالت تاریک';
                }
            }"""

old_shadow_loop = """            document.querySelectorAll('*').forEach(function(el) {
                if (el.shadowRoot) {
                    var s = el.shadowRoot.getElementById('hermes-shadow-style');
                    if (!s) {
                        s = document.createElement('style');
                        s.id = 'hermes-shadow-style';
                        el.shadowRoot.appendChild(s);
                    }
                    s.textContent = shadowCss;
                }
            });"""

new_shadow_loop = """            document.querySelectorAll('*').forEach(function(el) {
                if (el.shadowRoot) {
                    var contentsEl = el.shadowRoot.querySelector('.contents');
                    if (contentsEl) {
                        if (isDark) {
                            contentsEl.classList.remove('light');
                            contentsEl.classList.add('dark');
                        } else {
                            contentsEl.classList.remove('dark');
                            contentsEl.classList.add('light');
                        }
                    }
                    var s = el.shadowRoot.getElementById('hermes-shadow-style');
                    if (!s) {
                        s = document.createElement('style');
                        s.id = 'hermes-shadow-style';
                        el.shadowRoot.appendChild(s);
                    }
                    s.textContent = shadowCss;
                }
            });"""

old_prompts = """    _prompts = [
        "لطفاً با استفاده از ابزار execute_command، دستور whoami را اجرا کن.",
        "وضعیت سلامت سیستم را با ابزار get_system_health بررسی کن.",
        "مجموع اعداد ۱۲ و ۲۸ را با ابزار math_add حساب کن.",
        "تبدیل دمای ۳۷ درجه سانتی‌گراد به فارنهایت را با unit_celsius_to_fahrenheit انجام بده."
    ]"""

new_prompts = """    _prompts = [
        "آسیب‌پذیری تزریق SQL را تحلیل و روش پیاده‌سازی امن با Prepared Statements در پایتون را با ابزار دیتابیس تست کن.",
        "با ابزار execute_command شناسه کاربری و سطوح دسترسی (id و whoami) را بررسی و خطرات دسترسی روت را تحلیل نما.",
        "یک تحلیل امنیتی از مبهم‌سازی با Base64 و هشینگ SHA-256 ارائه بده و با str_sha256 توکن نشست را محاسبه کن.",
        "مکانیزم دفاعی در برابر Brute-Force را با الگوریتم Token Bucket در پایتون شبیه‌سازی کن."
    ]"""

if old_snippet in content:
    content = content.replace(old_snippet, new_snippet)
    print("Replaced snippet successfully")
else:
    print("old_snippet not found!")

if old_shadow_loop in content:
    content = content.replace(old_shadow_loop, new_shadow_loop)
    print("Replaced shadow loop successfully")
else:
    print("old_shadow_loop not found!")

if old_prompts in content:
    content = content.replace(old_prompts, new_prompts)
    print("Replaced prompts successfully")
else:
    print("old_prompts not found!")

notebook_path.write_text(content, encoding="utf-8")
print("Saved notebook.py successfully")
