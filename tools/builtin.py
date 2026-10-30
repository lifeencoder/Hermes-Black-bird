#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hermes Black Bird - Builtin Tools
Core tools for time queries and arithmetic calculation.
Pure Python - zero external UI dependencies.
"""

import ast
import operator
import time
from datetime import datetime
from typing import Any, Dict, Optional

from tools.registry import ToolRegistry


# ------------------------------------------------------------------------------
# 1. get_current_time
# ------------------------------------------------------------------------------
def get_current_time() -> str:
    """
    \u062f\u0631\u06cc\u0627\u0641\u062a \u0632\u0645\u0627\u0646 \u0648 \u062a\u0627\u0631\u06cc\u062e \u0641\u0639\u0644\u06cc \u0633\u06cc\u0633\u062a\u0645 \u0628\u0647 \u0635\u0648\u0631\u062a \u0633\u0627\u062e\u062a\u0627\u0631\u06cc\u0627\u0641\u062a\u0647.
    """
    now = datetime.now()
    return (
        f"\u062a\u0627\u0631\u06cc\u062e \u0648 \u0633\u0627\u0639\u062a \u0641\u0639\u0644\u06cc: {now.strftime('%Y-%m-%d %H:%M:%S')} "
        f"(\u0631\u0648\u0632: {now.strftime('%A')})"
    )


# ------------------------------------------------------------------------------
# 2. calculate (Safe Math Expression Evaluator)
# ------------------------------------------------------------------------------
_ALLOWED_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _eval_ast(node: ast.AST) -> Any:
    if isinstance(node, ast.Expression):
        return _eval_ast(node.body)
    elif isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.BinOp):
        left = _eval_ast(node.left)
        right = _eval_ast(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPS:
            return _ALLOWED_OPS[op_type](left, right)
        raise ValueError(f"\u0639\u0645\u0644\u06af\u0631 \u067e\u0634\u062a\u06cc\u0628\u0627\u0646\u06cc\u200c\u0646\u0634\u062f\u0647: {op_type.__name__}")
    elif isinstance(node, ast.UnaryOp):
        operand = _eval_ast(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPS:
            return _ALLOWED_OPS[op_type](operand)
        raise ValueError(f"\u0639\u0645\u0644\u06af\u0631 \u067e\u0634\u062a\u06cc\u0628\u0627\u0646\u06cc\u200c\u0646\u0634\u062f\u0647: {op_type.__name__}")
    else:
        raise ValueError(f"\u0639\u0628\u0627\u0631\u062a \u0646\u0627\u0645\u0639\u062a\u0628\u0631: {type(node).__name__}")


def calculate(expression: str) -> str:
    """
    \u0645\u062d\u0627\u0633\u0628\u0647 \u0639\u0628\u0627\u0631\u0627\u062a \u0631\u06cc\u0627\u0636\u06cc \u0633\u0627\u062f\u0647 \u0645\u0627\u0646\u0646\u062f \u062c\u0645\u0639\u060c \u062a\u0641\u0631\u06cc\u0642\u060c \u0636\u0631\u0628\u060c \u062a\u0642\u0633\u06cc\u0645 \u0648 \u062a\u0648\u0627\u0646.
    """
    cleaned = expression.strip()
    persian_digits = "\u06f0\u06f1\u06f2\u06f3\u06f4\u06f5\u06f6\u06f7\u06f8\u06f9"
    arabic_digits = "\u0660\u0661\u0662\u0663\u0664\u0665\u0666\u0667\u0668\u0669"
    for i in range(10):
        cleaned = cleaned.replace(persian_digits[i], str(i))
        cleaned = cleaned.replace(arabic_digits[i], str(i))

    # Replace unicode multiplication/division/power symbols
    cleaned = cleaned.replace("\u00d7", "*").replace("\u00f7", "/").replace("^", "**")

    try:
        parsed = ast.parse(cleaned, mode="eval")
        result = _eval_ast(parsed)
        return str(result)
    except Exception as err:
        return f"\u062e\u0637\u0627 \u062f\u0631 \u0645\u062d\u0627\u0633\u0628\u0647 '{expression}': {str(err)}"


# ------------------------------------------------------------------------------
# Registration Function & Default Registry
# ------------------------------------------------------------------------------
def register_builtin_tools(registry: Optional[ToolRegistry] = None) -> ToolRegistry:
    """
    Register standard builtin tools into the provided or newly created ToolRegistry.
    """
    if registry is None:
        registry = ToolRegistry()

    # Register get_current_time
    registry.register(
        name="get_current_time",
        description="\u062f\u0631\u06cc\u0627\u0641\u062a \u062a\u0627\u0631\u06cc\u062e \u0648 \u0632\u0645\u0627\u0646 \u062f\u0642\u06cc\u0642 \u0641\u0639\u0644\u06cc \u0633\u06cc\u0633\u062a\u0645.",
        parameters={
            "type": "object",
            "properties": {},
            "required": [],
        },
        func=get_current_time,
    )

    # Register calculate
    registry.register(
        name="calculate",
        description="\u0645\u062d\u0627\u0633\u0628\u0647 \u062f\u0642\u06cc\u0642 \u0639\u0628\u0627\u0631\u0627\u062a \u0631\u06cc\u0627\u0636\u06cc \u0634\u0627\u0645\u0644 \u062c\u0645\u0639 (+)\u060c \u062a\u0641\u0631\u06cc\u0642 (-)\u060c \u0636\u0631\u0628 (*)\u060c \u062a\u0642\u0633\u06cc\u0645 (/)\u060c \u062a\u0648\u0627\u0646 (**). \u0645\u062b\u0627\u0644: '25 * 4'.",
        parameters={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "\u0639\u0628\u0627\u0631\u062a \u0631\u06cc\u0627\u0636\u06cc \u062c\u0647\u062a \u0645\u062d\u0627\u0633\u0628\u0647\u060c \u0628\u0631\u0627\u06cc \u0645\u062b\u0627\u0644 '25 * 4' \u06cc\u0627 '(10 + 5) / 3'",
                }
            },
            "required": ["expression"],
        },
        func=calculate,
    )

    return registry


builtin_registry = register_builtin_tools()
