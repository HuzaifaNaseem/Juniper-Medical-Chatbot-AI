@echo off
echo ============================================================
echo JUNIPER - Medical Research Assistant
echo Quick Start Script for Windows
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [1/5] Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
    echo.
) else (
    echo [1/5] Virtual environment already exists.
    echo.
)

REM Activate virtual environment
echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo [3/5] Installing dependencies...
echo This may take a few minutes on first run...
pip install -r requirements.txt > nul 2>&1
if %errorlevel% equ 0 (
    echo Dependencies installed successfully.
) else (
    echo Error installing dependencies. Please check your internet connection.
    pause
    exit /b 1
)
echo.

REM Check if .env exists
if not exist ".env" (
    echo [4/5] Creating .env file...
    copy .env.example .env > nul
    echo.
    echo ============================================================
    echo IMPORTANT: Please edit .env file and add your Groq API key!
    echo Get your free API key at: https://console.groq.com
    echo ============================================================
    echo.
    echo Press any key to open .env file in notepad...
    pause > nul
    notepad .env
    echo.
) else (
    echo [4/5] .env file already exists.
    echo.
)

REM Initialize knowledge base
if not exist "data\chroma_db" (
    echo [5/5] Initializing knowledge base...
    echo This will take 2-5 minutes on first run...
    python initialize_kb.py
    if %errorlevel% neq 0 (
        echo.
        echo Error initializing knowledge base.
        echo Please make sure you have added your Groq API key to .env file.
        pause
        exit /b 1
    )
) else (
    echo [5/5] Knowledge base already initialized.
    echo.
)

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Starting Juniper...
echo Access the application at: http://localhost:5000
echo Press CTRL+C to stop the server
echo.
echo ============================================================
echo.

REM Run the application
python app.py

pause
