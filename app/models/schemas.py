from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    question: str
    use_rag: bool = True

class ChatResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = []

class UploadResponse(BaseModel):
    filename: str
    chunks_count: int
    message: str