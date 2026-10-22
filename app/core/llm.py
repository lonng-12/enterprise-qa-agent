from openai import OpenAI
from app.config import settings

client = OpenAI(
    api_key=settings.DEEPSEEK_API_KEY,
    base_url=settings.DEEPSEEK_BASE_URL
)

SYSTEM_PROMPT = """你是一个企业知识库助手。请严格根据提供的知识库内容回答用户问题。
如果知识库中没有相关信息，请如实说明，不要编造。
回答时请引用来源文档名称。"""

def build_prompt(question: str, context_chunks: list) -> str:
    context = "\n\n".join([f"[来源文档]\n{c}" for c in context_chunks])
    return f"""【知识库内容】
{context}

【用户问题】
{question}

请基于以上知识库内容回答问题。"""

def chat_stream(question: str, context_chunks: list = None):
    """流式对话"""
    if context_chunks:
        user_content = build_prompt(question, context_chunks)
    else:
        user_content = question

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ],
        stream=True,
        temperature=0.3
    )

    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content