#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hermes Black Bird - Tool Registry
A lightweight, extensible registry for registering Python functions and schemas
conforming to the OpenAI Tool Calling / Model Context Protocol (MCP) standard.
Pure Python - zero external UI dependencies.
"""

import json
from typing import Any, Callable, Dict, List, Optional, Union


class ToolRegistry:
    """
    Registry for managing and executing tools available to the LLM agent.
    Supports both native Python functions and remote Model Context Protocol (MCP) tools.
    """

    def __init__(self):
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._functions: Dict[str, Callable] = {}

    def register(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        func: Callable,
    ) -> None:
        """
        Register a function as a tool with OpenAI-compatible schema.

        Args:
            name: Unique identifier of the function.
            description: Concise explanation of what the tool does.
            parameters: JSON Schema dictionary defining arguments.
            func: The actual Python callable.
        """
        tool_definition = {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters,
            },
        }
        self._tools[name] = tool_definition
        self._functions[name] = func

    def register_mcp_tools(self, mcp_client: Any) -> List[str]:
        """
        Discover and register all tools from an MCPClient into this registry.

        Args:
            mcp_client: MCPClient instance (with list_tools() and call_tool() methods).

        Returns:
            List of registered tool names.
        """
        mcp_tools = mcp_client.list_tools()
        registered_names: List[str] = []

        for tool_info in mcp_tools:
            name = tool_info["name"]
            description = tool_info.get("description", f"MCP Tool: {name}")
            parameters = tool_info.get("parameters") or {
                "type": "object",
                "properties": {},
            }

            # Create closure for delegating tool execution to mcp_client
            def make_proxy(tool_name: str):
                return lambda **kwargs: mcp_client.call_tool(tool_name, kwargs)

            self.register(
                name=name,
                description=description,
                parameters=parameters,
                func=make_proxy(name),
            )
            registered_names.append(name)

        return registered_names

    def tool(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
    ):
        """
        Decorator to register a function as a tool.
        """
        def decorator(func: Callable):
            tool_name = name or func.__name__
            tool_desc = description or (func.__doc__.strip() if func.__doc__ else f"Tool: {tool_name}")
            tool_params = parameters or {
                "type": "object",
                "properties": {},
                "required": [],
            }
            self.register(tool_name, tool_desc, tool_params, func)
            return func

        return decorator

    def get_tools(self) -> List[Dict[str, Any]]:
        """
        Return the list of all registered tools formatted for OpenAI API.
        """
        return list(self._tools.values())

    def has_tool(self, name: str) -> bool:
        """
        Check if a tool is registered.
        """
        return name in self._functions

    def list_tool_names(self) -> List[str]:
        """
        List all registered tool names.
        """
        return list(self._functions.keys())

    def execute(self, name: str, arguments: Union[str, Dict[str, Any]]) -> str:
        """
        Execute a registered tool by name with provided arguments.

        Args:
            name: Tool name to execute.
            arguments: JSON string or dict containing parameters.

        Returns:
            String result (or JSON string) of the execution.
        """
        if name not in self._functions:
            return json.dumps({
                "status": "error",
                "error": f"Tool '{name}' is not registered."
            }, ensure_ascii=False)

        # Parse JSON string arguments if necessary
        if isinstance(arguments, str):
            try:
                args = json.loads(arguments) if arguments.strip() else {}
            except Exception as e:
                return json.dumps({
                    "status": "error",
                    "error": f"Failed to parse arguments JSON: {str(e)}"
                }, ensure_ascii=False)
        elif isinstance(arguments, dict):
            args = arguments
        else:
            args = {}

        func = self._functions[name]
        try:
            result = func(**args)
            if isinstance(result, (dict, list)):
                return json.dumps(result, ensure_ascii=False)
            return str(result)
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error": f"Error executing tool '{name}': {str(e)}"
            }, ensure_ascii=False)
