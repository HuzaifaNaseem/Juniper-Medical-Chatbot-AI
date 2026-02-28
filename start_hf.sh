#!/bin/bash
echo "Initializing Knowledge Base..."
python initialize_kb.py
echo "Starting Application on port 7860..."
gunicorn wsgi:application --bind 0.0.0.0:7860 --workers 2 --worker-class gevent --timeout 120 --log-level info
