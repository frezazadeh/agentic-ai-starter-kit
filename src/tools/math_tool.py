from __future__ import annotations

import math
from typing import Literal, TypedDict


class MathRequest(TypedDict):
    """Schema the model will use when calling our tool."""
    expression: str
    mode: Literal["eval", "sqrt", "factorial"]


def evaluate_math(payload: MathRequest) -> str:
    """
    Very small, safe-ish math executor.
    - mode='eval': evaluate simple arithmetic only (digits + operators).
    - mode='sqrt': compute square root.
    - mode='factorial': compute factorial (small ints).
    """
    expr = payload["expression"]
    mode = payload["mode"]

    if mode == "sqrt":
        try:
            return str(math.sqrt(float(expr)))
        except Exception as e:
            return f"Error: {e}"

    if mode == "factorial":
        try:
            n = int(expr)
            if n < 0 or n > 10000:
                return "Error: n out of range"
            return str(math.factorial(n))
        except Exception as e:
            return f"Error: {e}"

    if mode == "eval":
        # allow only digits, parentheses, spaces, and basic operators
        allowed = set("0123456789+-*/(). ")
        if not set(expr) <= allowed:
            return "Error: disallowed characters"
        try:
            return str(eval(expr, {"__builtins__": {}}, {}))  # noqa: S307 (we sandbox)
        except Exception as e:
            return f"Error: {e}"

    return "Error: unknown mode"
