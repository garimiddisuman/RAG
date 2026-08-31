from langchain_text_splitters import MarkdownHeaderTextSplitter


HEADERS_TO_SPLIT_ON = [
  ("#", "heading_1"),
  ("##", "heading_2"),
  ("###", "heading_3"),
]


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