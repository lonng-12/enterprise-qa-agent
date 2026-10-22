import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from pathlib import Path
from dotenv import load_dotenv

# BASE_DIR = D:\enterprise-qa-agent
BASE_DIR = Path(__file__).resolve().parent.parent

# 明确读取项目根目录下的 .env
load_dotenv(str(BASE_DIR / ".env"))

class Settings:
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

    # 所有数据都写到 D:\enterprise-qa-agent 下面
    CHROMA_PERSIST_DIR = str(BASE_DIR / "chroma_db")
    UPLOAD_DIR = str(BASE_DIR / "data" / "uploads")

    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    TOP_K = 3

settings = Settings()