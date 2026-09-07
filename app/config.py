from pathlib import Path


APP_DIR = Path(__file__).resolve().parent.parent

DOCUMENTS_DIR = APP_DIR / "data" / "documents"

CHROMA_PERSISTENCE_DIR = (
    Path.home()
    / "Library"
    / "Application Support"
    / "my-rag"
    / "chroma_db"
)

EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.2"

CHROMA_COLLECTION_NAME = "company_documents"