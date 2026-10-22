import json
from app.core.llm import client
from app.core.tools import TOOLS, execute_tool

AGENT_PROMPT = """你是一个智能助手，可以调用工具来帮助用户。
如果需要数学计算，请调用 calculate 工具。
如果问题涉及企业知识，请基于提供的知识库内容回答。"""

def run_agent(question: str, context_chunks: list = None):
    """Agent 主循环：判断是否需要调用工具"""
    messages = [{"role": "system", "content": AGENT_PROMPT}]

    if context_chunks:
        context = "\n\n".join(context_chunks)
        messages.append({"role": "system", "content": f"知识库内容:\n{context}"})

    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=TOOLS,
        temperature=0.3
    )

    msg = response.choices[0].message

    if msg.tool_calls:
        tool_call = msg.tool_calls[0]

        try:
            args = json.loads(tool_call.function.arguments or "{}")
        except json.JSONDecodeError:
            args = {}

        tool_result = execute_tool(tool_call.function.name, args)

        messages.append(msg)
        messages.append({
            "role": "tool",
            "content": tool_result,
            "tool_call_id": tool_call.id
        })

        final = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.3
        )
        return final.choices[0].message.content

    return msg.content