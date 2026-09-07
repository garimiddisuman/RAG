from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from app.config import (
  CHROMA_COLLECTION_NAME,
  CHROMA_PERSISTENCE_DIR,
  EMBEDDING_MODEL,
)

from app.ingestion.document_processor import (
  load_documents,
  chunk_documents,
)


def create_embeddings():
  return OllamaEmbeddings(
    model=EMBEDDING_MODEL,
  )


def create_vector_store():
  embeddings = create_embeddings()

  return Chroma(
    collection_name=CHROMA_COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=CHROMA_PERSISTENCE_DIR,
  )


def add_documents(documents):
  vector_store = create_vector_store()
  vector_store.add_documents(documents)

  return vector_store


def ingest_documents():
  documents = load_documents()
  chunks = chunk_documents(documents)

  return add_documents(chunks)


def is_vector_store_initialized():
  vector_store = create_vector_store()

  return vector_store._collection.count() > 0


def initialize_vector_store():
  if not is_vector_store_initialized():
    ingest_documents()


if __name__ == "__main__":
  ingest_documents()