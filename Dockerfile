# Use official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file separately to cache dependencies
COPY requirements.txt .

# Install Python dependencies
# Adding gunicorn for production serving
RUN pip install --no-cache-dir -r requirements.txt gunicorn gevent

# Copy the rest of the application code
COPY . .

# Set environment variables for Hugging Face Spaces
# Spaces expose port 7860 by default
ENV PORT=7860
ENV FLASK_ENV=production
ENV AUTO_INIT=1
# Ensure Python outputs everything immediately to the logs
ENV PYTHONUNBUFFERED=1

# Expose the standard HF Spaces port
EXPOSE 7860

# We need to make sure the data and chroma_db directories have write permissions
# HuggingFace spaces run as user 1000
RUN mkdir -p /app/data /app/chroma_db && \
    chmod -R 777 /app/data /app/chroma_db

# Create a startup script to initialize KB safely and run the app
RUN echo '#!/bin/bash\n\
echo "Initializing Knowledge Base..."\n\
python initialize_kb.py\n\
echo "Starting Application on port 7860..."\n\
gunicorn wsgi:application --bind 0.0.0.0:7860 --workers 2 --worker-class gevent --timeout 120 --log-level info\n\
' > /app/start.sh && chmod +x /app/start.sh

# Run the startup script
CMD ["/app/start.sh"]
