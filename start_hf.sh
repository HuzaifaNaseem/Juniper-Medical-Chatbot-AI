#!/bin/bash
set -e
echo "=== Juniper Medical Bot Startup ==="
echo "Initializing Knowledge Base..."
python initialize_kb.py
echo "Knowledge Base initialized."
echo "Starting Application on port 7860..."
exec gunicorn wsgi:application --bind 0.0.0.0:7860 --workers 1 --worker-class gevent --timeout 300 --log-level debug
