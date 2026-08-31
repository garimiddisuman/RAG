from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter


DOCUMENTS_DIR = Path("documents")


loader = DirectoryLoader(
  str(DOCUMENTS_DIR),
  glob="**/*.md",
  loader_cls=TextLoader,
  loader_kwargs={"encoding": "utf-8"},
)

documents = loader.load()


headers_to_split_on = [
  ("#", "heading_1"),
  ("##", "heading_2"),
  ("###", "heading_3"),
]

splitter = MarkdownHeaderTextSplitter(
  headers_to_split_on=headers_to_split_on,
)

chunks = []

for document in documents:
  document_chunks = splitter.split_text(document.page_content)

  for chunk in document_chunks:
    chunk.metadata["source"] = document.metadata["source"]

  chunks.extend(document_chunks)


print(f"Documents: {len(documents)}")
print(f"Chunks: {len(chunks)}")

for index, chunk in enumerate(chunks):
  print("\n" + "-" * 60)
  print(f"Chunk: {index + 1}")
  print(f"Metadata: {chunk.metadata}")
  print(f"Content:\n{chunk.page_content}")