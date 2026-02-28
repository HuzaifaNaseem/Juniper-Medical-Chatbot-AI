"""
WSGI Entry Point for Production Deployment
"""

from app import app, startup
import sys

# Initialize application on startup
if not startup():
    print("WARNING: Failed to fully initialize application. App will run in degraded mode.")
    print("Chat functionality may not work until GROQ_API_KEY is configured.")

# WSGI application
application = app

if __name__ == "__main__":
    app.run()
