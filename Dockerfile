FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential dos2unix && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn gevent

# Pre-download the sentence-transformers model into the Docker image.
# This prevents slow/failed downloads when the container starts on HF Spaces.
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2'); print('Model pre-downloaded OK')"

COPY . .

# Fix Windows line endings that break bash scripts
RUN dos2unix /app/start_hf.sh || true
RUN dos2unix /app/*.py || true
RUN dos2unix /app/backend/*.py || true

# Create data dir and pre-initialize ChromaDB with medical knowledge during build.
# No GROQ_API_KEY is needed for this step — only for the LLM at runtime.
# At startup, initialize_kb.py will detect existing data and skip (AUTO_INIT=1).
RUN mkdir -p /app/data/chroma_db
RUN python initialize_kb.py

# Make data directories writable for HF Spaces (runs as uid 1000)
RUN chmod -R 777 /app/data
RUN chmod +x /app/start_hf.sh

ENV PORT=7860
ENV FLASK_ENV=production
ENV AUTO_INIT=1
ENV PYTHONUNBUFFERED=1

EXPOSE 7860

CMD ["bash", "/app/start_hf.sh"]
