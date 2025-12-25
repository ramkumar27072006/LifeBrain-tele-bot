# utils/solver.py
import math

def solve_expression(expr: str) -> str:
    """
    Safely evaluate mathematical expressions using math.* functions.
    Avoids __builtins__ for safety.
    """
    try:
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        result = eval(expr, {"__builtins__": {}}, allowed_names)
        return f"🧮 Result: {result}"
    except Exception as e:
        return f"❌ Error: {e}"
