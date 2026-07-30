import os
from dotenv import load_dotenv

load_dotenv()

# --- Paths ---
RAW_DATA_DIR = "data/raw"
CHROMA_DB_DIR = "chroma_db"
COLLECTION_NAME = "my_knowledge_base"

# --- Chunking ---
CHUNK_SIZE = 500       # characters per chunk
CHUNK_OVERLAP = 50      # overlap between chunks to preserve context

# --- Retrieval ---
TOP_K = 5               # number of chunks to retrieve per query

# --- Embedding ---
# Option A: local embedding model (no API key needed)
EMBEDDING_MODE = "local"   # "local" or "gemini"
LOCAL_EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Option B: Gemini embedding (if EMBEDDING_MODE = "gemini")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_EMBEDDING_MODEL = "models/text-embedding-004"

# --- Generation (LLM) ---
GENERATION_PROVIDER = "gemini"   # "gemini" or "deepseek"
GEMINI_GENERATION_MODEL = "gemini-2.0-flash"

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"
