import chromadb
from chromadb.utils import embedding_functions
from app.config import settings

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self.collection = self.client.get_or_create_collection(
            name="knowledge_base",
            embedding_function=self.embedding_fn
        )

    def add_documents(self, chunks: list, source: str):
        """将文档切片加入向量库"""
        ids = [f"{source}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": source} for _ in chunks]
        self.collection.add(documents=chunks, ids=ids, metadatas=metadatas)

    def search(self, query: str, top_k: int = None):
        """相似度检索"""
        top_k = top_k or settings.TOP_K
        results = self.collection.query(query_texts=[query], n_results=top_k)
        return results["documents"][0] if results["documents"] else []