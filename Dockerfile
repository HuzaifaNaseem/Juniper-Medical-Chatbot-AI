FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential dos2unix && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn gevent

COPY . .

# Fix Windows line endings that break bash scripts
RUN dos2unix /app/start_hf.sh || true
RUN dos2unix /app/*.py || true
RUN dos2unix /app/backend/*.py || true

ENV PORT=7860
ENV FLASK_ENV=production
ENV AUTO_INIT=1
ENV PYTHONUNBUFFERED=1

EXPOSE 7860

# Make data directories writable by any user (HF runs as user 1000)
RUN mkdir -p /app/data/chroma_db && chmod -R 777 /app/data
RUN chmod +x /app/start_hf.sh

CMD ["bash", "/app/start_hf.sh"]
