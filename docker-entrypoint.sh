#!/bin/sh
set -e

ollama serve >/var/log/ollama.log 2>&1 &
OLLAMA_PID=$!
trap 'kill $OLLAMA_PID 2>/dev/null || true' EXIT

until ollama list >/dev/null 2>&1; do
  sleep 1
done

if [ ! -f /rag/app/chroma_db/chroma.sqlite3 ]; then
  echo "chroma_db empty, running ingestion..."
  python -m app.ingestion.store
fi

python -m app.graph.graph
