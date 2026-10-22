import os
from pypdf import PdfReader
from app.config import settings

def parse_document(file_path: str) -> str:
    """解析 PDF 或 TXT 文档"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    elif ext == ".txt":
        # 加上 errors="ignore" 容错，或者用 gbk 编码读取
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    raise ValueError(f"不支持的文件格式: {ext}")

def split_text(text: str, chunk_size: int = None, overlap: int = None) -> list:
    """将长文本切分为重叠的片段"""
    chunk_size = chunk_size or settings.CHUNK_SIZE
    overlap = overlap or settings.CHUNK_OVERLAP
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return [c.strip() for c in chunks if c.strip()]