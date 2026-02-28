#!/bin/bash
# Startup script for DigitalOcean deployment

echo "========================================"
echo "Juniper - Medical Research Assistant"
echo "DigitalOcean Deployment Startup"
echo "========================================"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found!"
    echo "Please create .env file with your GROQ_API_KEY"
    exit 1
fi

# Initialize knowledge base if needed
if [ ! -d "data/chroma_db" ] || [ -z "$(ls -A data/chroma_db 2>/dev/null)" ]; then
    echo ""
    echo "Initializing knowledge base..."
    python3 initialize_kb.py
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to initialize knowledge base"
        exit 1
    fi
fi

echo ""
echo "Starting Gunicorn server..."
echo "========================================"

# Start Gunicorn with optimal settings for DigitalOcean
exec gunicorn wsgi:application \
    --bind 0.0.0.0:${PORT:-8080} \
    --workers 4 \
    --worker-class gevent \
    --worker-connections 1000 \
    --timeout 120 \
    --keep-alive 5 \
    --log-level info \
    --access-logfile - \
    --error-logfile -
