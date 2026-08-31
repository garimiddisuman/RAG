from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter

from app.config import DOCUMENTS_DIR


HEADERS_TO_SPLIT_ON = [
  ("#", "heading_1"),
  ("##", "heading_2"),
  ("###", "heading_3"),
]


def load_documents():
  loader = DirectoryLoader(
    str(DOCUMENTS_DIR),
    glob="**/*.md",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"},
  )

  return loader.load()


def chunk_documents(documents):
  splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=HEADERS_TO_SPLIT_ON,
  )

  chunks = []

  for document in documents:
    document_chunks = splitter.split_text(document.page_content)

    for chunk in document_chunks:
      chunk.metadata["source"] = document.metadata.get("source")

    chunks.extend(document_chunks)

  return chunks