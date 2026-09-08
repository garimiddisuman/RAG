from pathlib import Path


DOCUMENTS_DIR = Path("documents")
CHROMA_PERSISTENCE_DIR = "./app/chroma_db"

EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.2"

CHROMA_COLLECTION_NAME = "company_documents"