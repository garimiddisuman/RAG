from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from app.config import (
  CHROMA_COLLECTION_NAME,
  CHROMA_PERSISTENCE_DIR,
  EMBEDDING_MODEL,
)

from app.ingestion.store import create_vector_store


def search(query, k=3):
  vector_store = create_vector_store()

  return vector_store.similarity_search(
    query,
    k=k,
  )


if __name__ == "__main__":
  query = "How many annual leave days do employees get?"

  results = search(query)

  print(f"Query: {query}")

  for index, document in enumerate(results):
    print("\n" + "-" * 60)
    print(f"Result {index + 1}")
    print(f"Source: {document.metadata.get('source')}")
    print(f"Section: {document.metadata.get('heading_2')}")
    print(f"\n{document.page_content}")