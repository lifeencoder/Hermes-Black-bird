#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hermes Black Bird - Agent Runner
Autonomous tool-calling execution loop orchestrator.
Pure Python - zero external UI dependencies.
"""

import json
from typing import Any, Callable, Dict, Generator, List, Optional
from client.model_client import ModelClient
from tools.registry import ToolRegistry


class AgentRunner:
    """
    Manages the conversational loop between ModelClient and ToolRegistry,
    automatically resolving multi-step tool calls until final synthesis.
    """

    def __init__(
        self,
        model_client: ModelClient,
        tool_registry: Optional[ToolRegistry] = None,
        max_iterations: int = 5,
    ):
        """
        Initialize the AgentRunner.

        Args:
            model_client: Configured ModelClient instance.
            tool_registry: ToolRegistry containing available functions.
            max_iterations: Safety ceiling to prevent infinite tool-call loops.
        """
        self.client = model_client
        self.registry = tool_registry or ToolRegistry()
        self.max_iterations = max_iterations

    def run(
        self,
        messages: List[Dict[str, Any]],
        verbose: bool = True,
        on_tool_call: Optional[Callable[[str, Any, str], None]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Execute the agent loop:
        1. Query model with messages and available tool definitions.
        2. If model calls tools, execute them via registry.
        3. Append assistant tool_calls and tool results to history.
        4. Repeat until model generates final response or max iterations reached.

        Args:
            messages: Conversation messages list.
            verbose: Whether to print tool-calling progress to stdout.
            on_tool_call: Optional callback: fn(tool_name, arguments, result).
            **kwargs: Extra parameters passed to model_client.chat.

        Returns:
            Dict containing 'content', 'history', 'iterations', and 'executed_tools'.
        """
        # Shallow copy messages so input isn't modified unexpectedly
        history: List[Dict[str, Any]] = list(messages)
        tools = self.registry.get_tools() if self.registry else None
        executed_tools: List[Dict[str, Any]] = []

        for iteration in range(1, self.max_iterations + 1):
            if verbose:
                print(f"[*] [AgentRunner] Iteration {iteration}/{self.max_iterations} - Querying model...")

            # In tool execution loop, use non-streaming to inspect tool_calls cleanly
            response = self.client.chat(
                messages=history,
                tools=tools,
                stream=False,
                **kwargs,
            )

            choice = response.choices[0]
            message = choice.message

            # Check if model requested tool call(s)
            if hasattr(message, "tool_calls") and message.tool_calls:
                tool_calls = message.tool_calls
                if verbose:
                    print(f"    [+] Model requested {len(tool_calls)} tool call(s).")

                # 1. Append assistant tool_calls message to history
                assistant_record: Dict[str, Any] = {
                    "role": "assistant",
                    "content": message.content or None,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": getattr(tc, "type", "function"),
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            },
                        }
                        for tc in tool_calls
                    ],
                }
                history.append(assistant_record)

                # 2. Execute each tool and append tool response
                for tc in tool_calls:
                    tool_name = tc.function.name
                    tool_args = tc.function.arguments

                    if verbose:
                        print(f"    --> Executing Tool: '{tool_name}' with args: {tool_args}")

                    tool_result = self.registry.execute(tool_name, tool_args)

                    if verbose:
                        preview = str(tool_result)[:120] + ("..." if len(str(tool_result)) > 120 else "")
                        print(f"    <-- Result: {preview}")

                    executed_tools.append({
                        "iteration": iteration,
                        "name": tool_name,
                        "arguments": tool_args,
                        "result": tool_result,
                    })

                    if on_tool_call:
                        try:
                            on_tool_call(tool_name, tool_args, tool_result)
                        except Exception:
                            pass

                    # Standard OpenAI tool response message
                    history.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "name": tool_name,
                        "content": str(tool_result),
                    })

                # Proceed to next iteration to give model the tool results
                continue

            else:
                # No tool calls: model returned final synthesized response
                final_content = message.content or ""
                if verbose:
                    print(f"[*] [AgentRunner] Final answer generated at iteration {iteration}.")

                history.append({
                    "role": "assistant",
                    "content": final_content,
                })

                return {
                    "content": final_content,
                    "history": history,
                    "iterations": iteration,
                    "finish_reason": choice.finish_reason,
                    "executed_tools": executed_tools,
                    "status": "success",
                }

        # If max iterations reached without clean final response
        warning_msg = f"[AgentRunner] Warning: Maximum iterations ({self.max_iterations}) reached."
        if verbose:
            print(f"[!] {warning_msg}")

        return {
            "content": history[-1].get("content") or warning_msg,
            "history": history,
            "iterations": self.max_iterations,
            "finish_reason": "max_iterations",
            "executed_tools": executed_tools,
            "status": "max_iterations_reached",
        }

    def run_stream(
        self,
        messages: List[Dict[str, Any]],
        **kwargs,
    ) -> Generator[str, None, None]:
        """
        Streaming execution of the agent loop for reactive UI environments (e.g. Marimo).
        Yields status indicators when executing tools and then yields the final synthesized text.
        """
        history: List[Dict[str, Any]] = list(messages)
        tools = self.registry.get_tools() if self.registry else None

        for iteration in range(1, self.max_iterations + 1):
            response = self.client.chat(
                messages=history,
                tools=tools,
                stream=False,
                **kwargs,
            )

            choice = response.choices[0]
            message = choice.message

            # Check if model requested tool call(s)
            if hasattr(message, "tool_calls") and message.tool_calls:
                tool_calls = message.tool_calls
                assistant_record: Dict[str, Any] = {
                    "role": "assistant",
                    "content": message.content or None,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": getattr(tc, "type", "function"),
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            },
                        }
                        for tc in tool_calls
                    ],
                }
                history.append(assistant_record)

                for tc in tool_calls:
                    tool_name = tc.function.name
                    tool_args = tc.function.arguments

                    # Yield status indicator to the UI
                    yield f"🤖 **در حال فراخوانی ابزار `{tool_name}` از سرور MCP...**\n\n"

                    tool_result = self.registry.execute(tool_name, tool_args)

                    history.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "name": tool_name,
                        "content": str(tool_result),
                    })
                continue
            else:
                final_content = message.content or ""
                yield final_content
                return

        yield "⚠️ **حداکثر دفعات فراخوانی مجاز ابزارها به پایان رسید.**"
