"""
WSGI Entry Point for Production Deployment
"""

from app import app, startup
import sys

# Initialize application on startup
if not startup():
    print("ERROR: Failed to initialize application")
    sys.exit(1)

# WSGI application
application = app

if __name__ == "__main__":
    app.run()
