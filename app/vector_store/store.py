from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from app.ingestion.chunker import chunks


embeddings = OllamaEmbeddings(
  model="nomic-embed-text",
)

vector_store = Chroma(
  collection_name="company_documents",
  embedding_function=embeddings,
  persist_directory="./chroma_db",
)

vector_store.add_documents(chunks)

print(f"Stored {len(chunks)} chunks in ChromaDB")