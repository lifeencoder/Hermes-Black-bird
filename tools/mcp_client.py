#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hermes Black Bird - Standard Model Context Protocol (MCP) Client
Connects to external MCP servers over stdio, performs tool discovery,
and provides seamless synchronous and asynchronous tool execution for AgentRunner.
Pure Python - zero external UI dependencies.
"""

import asyncio
import json
import os
import sys
import threading
from typing import Any, Dict, List, Optional, Union

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    """
    Standard MCP Client managing a persistent stdio connection to an external MCP Server.
    Provides synchronous methods (list_tools, call_tool) compatible with ToolRegistry,
    bridging to an underlying asyncio event loop in a dedicated background thread.
    """

    def __init__(
        self,
        command: str,
        args: List[str],
        env: Optional[Dict[str, str]] = None,
        startup_timeout: float = 15.0,
    ):
        """
        Initialize the MCP Client configuration.

        Args:
            command: The executable command (e.g. 'python', 'node', 'uvx').
            args: Command-line arguments to pass to the MCP server.
            env: Optional environment variables dictionary.
            startup_timeout: Maximum seconds to wait for server initialization.
        """
        self.command = command
        self.args = args
        self.env = env or dict(os.environ)
        self.startup_timeout = startup_timeout

        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._stdio_cm = None
        self._session_cm = None
        self._session: Optional[ClientSession] = None
        self._is_connected = False
        self._lock = threading.Lock()

    def start(self) -> None:
        """
        Start the background event loop and establish connection to the MCP server.
        """
        with self._lock:
            if self._is_connected:
                return

            self._loop = asyncio.new_event_loop()
            self._thread = threading.Thread(target=self._run_event_loop, daemon=True)
            self._thread.start()

            future = asyncio.run_coroutine_threadsafe(
                self._async_connect(),
                self._loop
            )
            try:
                future.result(timeout=self.startup_timeout)
                self._is_connected = True
            except Exception as err:
                self.close()
                raise ConnectionError(f"Failed to connect to MCP server: {err}") from err

    def _run_event_loop(self) -> None:
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    async def _async_connect(self) -> None:
        params = StdioServerParameters(
            command=self.command,
            args=self.args,
            env=self.env,
        )
        self._stdio_cm = stdio_client(params)
        read_stream, write_stream = await self._stdio_cm.__aenter__()

        self._session_cm = ClientSession(read_stream, write_stream)
        self._session = await self._session_cm.__aenter__()

        await self._session.initialize()

    def list_tools(self) -> List[Dict[str, Any]]:
        """
        Discover and return all available tools exposed by the MCP server.
        Formatted with tool name, description, and inputSchema.
        """
        if not self._is_connected:
            self.start()

        async def _fetch():
            res = await self._session.list_tools()
            tools_list = []
            for t in res.tools:
                schema = (
                    getattr(t, "inputSchema", None)
                    or getattr(t, "parameters", None)
                    or {"type": "object", "properties": {}}
                )
                tools_list.append({
                    "name": t.name,
                    "description": t.description or f"MCP tool: {t.name}",
                    "parameters": schema,
                })
            return tools_list

        future = asyncio.run_coroutine_threadsafe(_fetch(), self._loop)
        return future.result(timeout=10.0)

    def call_tool(self, name: str, arguments: Union[str, Dict[str, Any]]) -> str:
        """
        Execute an MCP tool on the server with the specified arguments.

        Args:
            name: Name of the tool to execute.
            arguments: Dictionary or JSON string of arguments.

        Returns:
            String or JSON-encoded string representation of the tool output.
        """
        if not self._is_connected:
            self.start()

        if isinstance(arguments, str):
            try:
                args = json.loads(arguments) if arguments.strip() else {}
            except Exception:
                args = {}
        elif isinstance(arguments, dict):
            args = arguments
        else:
            args = {}

        async def _execute():
            res = await self._session.call_tool(name, arguments=args)
            output_parts = []
            for block in res.content:
                if hasattr(block, "text"):
                    output_parts.append(block.text)
                elif hasattr(block, "data"):
                    output_parts.append(str(block.data))
                else:
                    output_parts.append(str(block))
            return "\n".join(output_parts) if output_parts else "Success (no text output)"

        future = asyncio.run_coroutine_threadsafe(_execute(), self._loop)
        try:
            return future.result(timeout=30.0)
        except Exception as err:
            return json.dumps({
                "status": "error",
                "error": f"MCP execution error for '{name}': {str(err)}"
            }, ensure_ascii=False)

    def close(self) -> None:
        """
        Cleanly terminate the session and stop the background thread.
        """
        with self._lock:
            if not self._is_connected and not self._loop:
                return

            if self._loop and self._loop.is_running():
                async def _shutdown():
                    if self._session_cm:
                        try:
                            await self._session_cm.__aexit__(None, None, None)
                        except Exception:
                            pass
                    if self._stdio_cm:
                        try:
                            await self._stdio_cm.__aexit__(None, None, None)
                        except Exception:
                            pass

                try:
                    future = asyncio.run_coroutine_threadsafe(_shutdown(), self._loop)
                    future.result(timeout=5.0)
                except Exception:
                    pass
                finally:
                    self._loop.call_soon_threadsafe(self._loop.stop)

            self._is_connected = False
            self._session = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
