from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


embeddings = OllamaEmbeddings(
  model="nomic-embed-text",
)

vector_store = Chroma(
  collection_name="company_documents",
  embedding_function=embeddings,
  persist_directory="./chroma_db",
)

query = "How many annual leave days do employees get?"

results = vector_store.similarity_search(
  query,
  k=3,
)