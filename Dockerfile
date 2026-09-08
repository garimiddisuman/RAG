# syntax=docker/dockerfile:1.7

# ---------- Stage 1: ingestion ----------
# Loads Markdown from documents/, embeds with Ollama, writes app/chroma_db/.
FROM python:3.12-slim AS ingestion

WORKDIR /rag

RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY documents/ ./documents/

ENV OLLAMA_HOST=http://host.docker.internal:11434

RUN python -m app.ingestion.store


# ---------- Stage 2: runtime ----------
# Ships only app/ (including the pre-built app/chroma_db/). No Markdown docs.
FROM python:3.12-slim AS runtime

WORKDIR /rag

RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=ingestion /rag/app/ ./app/

ENV OLLAMA_HOST=http://host.docker.internal:11434
ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "app.graph.graph"]
