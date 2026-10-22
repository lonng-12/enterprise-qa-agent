def calculate(expression: str) -> str:
    """安全的数学计算工具"""
    try:
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expression):
            return "表达式包含不允许的字符"
        result = eval(expression)
        return f"计算结果: {result}"
    except Exception as e:
        return f"计算失败: {e}"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "数学表达式"}
                },
                "required": ["expression"]
            }
        }
    }
]

def execute_tool(name: str, arguments: dict) -> str:
    if name == "calculate":
        return calculate(arguments.get("expression", ""))
    return f"未知工具: {name}"