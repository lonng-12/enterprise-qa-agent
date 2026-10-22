import os
import shutil
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
from app.models.schemas import ChatRequest, ChatResponse, UploadResponse
from app.services.document import parse_document, split_text
from app.services.vectorstore import VectorStore
from app.core.llm import chat_stream
from app.core.agent import run_agent
from app.config import settings

router = APIRouter()
vector_store = VectorStore()

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = parse_document(file_path)
    chunks = split_text(text)
    vector_store.add_documents(chunks, source=file.filename)

    return UploadResponse(
        filename=file.filename,
        chunks_count=len(chunks),
        message="文档已成功导入知识库"
    )

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    context_chunks = []
    if req.use_rag:
        context_chunks = vector_store.search(req.question)

    answer = run_agent(req.question, context_chunks)
    sources = list(set([c[:30] for c in context_chunks])) if context_chunks else []

    return ChatResponse(answer=answer, sources=sources)

@router.post("/chat/stream")
async def chat_stream_endpoint(req: ChatRequest):
    context_chunks = vector_store.search(req.question) if req.use_rag else []
    return StreamingResponse(
        chat_stream(req.question, context_chunks),
        media_type="text/event-stream"
    )

@router.get("/health")
async def health():
    return {"status": "ok"}