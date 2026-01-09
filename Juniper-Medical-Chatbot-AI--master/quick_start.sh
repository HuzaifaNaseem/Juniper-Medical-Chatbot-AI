#!/bin/bash

echo "============================================================"
echo "JUNIPER - Medical Research Assistant"
echo "Quick Start Script for Mac/Linux"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[1/5] Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
    echo ""
else
    echo "[1/5] Virtual environment already exists."
    echo ""
fi

# Activate virtual environment
echo "[2/5] Activating virtual environment..."
source venv/bin/activate
echo ""

# Install dependencies
echo "[3/5] Installing dependencies..."
echo "This may take a few minutes on first run..."
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "Dependencies installed successfully."
else
    echo "Error installing dependencies. Please check your internet connection."
    exit 1
fi
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "[4/5] Creating .env file..."
    cp .env.example .env
    echo ""
    echo "============================================================"
    echo "IMPORTANT: Please edit .env file and add your Groq API key!"
    echo "Get your free API key at: https://console.groq.com"
    echo "============================================================"
    echo ""
    echo "Opening .env file for editing..."
    if command -v nano &> /dev/null; then
        nano .env
    elif command -v vi &> /dev/null; then
        vi .env
    else
        echo "Please edit .env file manually and add your Groq API key"
    fi
    echo ""
else
    echo "[4/5] .env file already exists."
    echo ""
fi

# Initialize knowledge base
if [ ! -d "data/chroma_db" ]; then
    echo "[5/5] Initializing knowledge base..."
    echo "This will take 2-5 minutes on first run..."
    python initialize_kb.py
    if [ $? -ne 0 ]; then
        echo ""
        echo "Error initializing knowledge base."
        echo "Please make sure you have added your Groq API key to .env file."
        exit 1
    fi
else
    echo "[5/5] Knowledge base already initialized."
    echo ""
fi

echo ""
echo "============================================================"
echo "Setup Complete!"
echo "============================================================"
echo ""
echo "Starting Juniper..."
echo "Access the application at: http://localhost:5000"
echo "Press CTRL+C to stop the server"
echo ""
echo "============================================================"
echo ""

# Run the application
python app.py
