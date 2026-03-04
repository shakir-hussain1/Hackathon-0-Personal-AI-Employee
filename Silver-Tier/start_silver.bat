@echo off
echo ========================================
echo   Silver Tier AI Employee Starting
echo ========================================
echo.

REM Ensure we run from Silver-Tier root regardless of launch location
cd /d "%~dp0"

REM ── Pre-flight: .env ─────────────────────────────────────────────────────────
if not exist ".env" (
    if exist ".env.example" (
        echo [WARN] .env not found. Copying from .env.example ...
        copy ".env.example" ".env" >nul
        echo [WARN] Please edit .env and fill in your values before continuing.
        echo.
    ) else (
        echo [WARN] .env not found and no .env.example to copy from.
        echo        Create a .env file based on the README before running.
        echo.
    )
)

REM ── Pre-flight: credentials.json ─────────────────────────────────────────────
if not exist "credentials.json" (
    echo [WARN] credentials.json not found.
    echo.
    echo        To set up Google Cloud credentials:
    echo        1. Go to https://console.cloud.google.com/
    echo        2. Create a project and enable Gmail + Calendar APIs
    echo        3. Create OAuth 2.0 credentials (Desktop app type)
    echo        4. Download the JSON and save as: Silver-Tier\credentials.json
    echo.
    echo        The orchestrator will start but Gmail/Calendar features
    echo        will be disabled until credentials.json is provided.
    echo.
)

REM ── Virtual environment setup ─────────────────────────────────────────────────
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
    echo Installing dependencies...
    venv\Scripts\pip install -r requirements.txt
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting Silver Tier Orchestrator...
echo Press Ctrl+C to stop.
echo.

python orchestrator\orchestrator.py

pause
