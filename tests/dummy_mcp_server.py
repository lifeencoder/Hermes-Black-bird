#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hermes Black Bird - Safe Dummy MCP Server for Testing
Exposes benign system diagnostics (CPU, RAM, OS platform) conforming to official MCP specification.
Compatible with both MCP 1.x (FastMCP) and MCP 2.x (MCPServer).
"""

import os
import platform
import sys

try:
    from mcp.server.fastmcp import FastMCP as ServerClass
except ImportError:
    from mcp.server.mcpserver import MCPServer as ServerClass

server = ServerClass("DummySystemInfoServer")


@server.tool(
    name="get_system_info",
    description="دریافت مشخصات سخت‌افزاری و سیستم‌عامل شامل نام پلتفرم، تعداد هسته‌های CPU، حافظه RAM و نسخه پایتون."
)
def get_system_info() -> str:
    """
    Return basic, safe diagnostic info about the host system environment.
    """
    total_ram = "نامشخص"
    # Check Linux /proc/meminfo for container environments (like MoLab)
    if os.path.exists("/proc/meminfo"):
        try:
            with open("/proc/meminfo", "r") as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        total_ram = line.split(":")[1].strip()
                        break
        except Exception:
            pass
    elif sys.platform == "win32":
        try:
            import ctypes
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]
            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
            total_ram = f"{round(stat.ullTotalPhys / (1024**3), 1)} GB"
        except Exception:
            pass

    return (
        f"سیستم‌عامل: {platform.system()} ({platform.release()} - {platform.machine()})\n"
        f"تعداد هسته‌های CPU: {os.cpu_count()}\n"
        f"میزان حافظه RAM: {total_ram}\n"
        f"نسخه مفسر پایتون: {sys.version.split()[0]}"
    )


if __name__ == "__main__":
    server.run(transport="stdio")
