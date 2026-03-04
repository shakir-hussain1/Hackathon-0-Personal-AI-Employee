@echo off
echo ============================================================
echo   Platinum Tier - Local Agent Starting
echo ============================================================
echo.

cd /d "%~dp0"

REM ── Pre-flight: .env ─────────────────────────────────────────
if not exist ".env" (
    if exist ".env.example" (
        echo [WARN] .env not found. Copying from .env.example...
        copy ".env.example" ".env" >nul
        echo [WARN] Edit .env before continuing (set VAULT_PATH etc.)
        echo.
        pause
        exit /b 1
    )
)

REM ── Pre-flight: vault folders ─────────────────────────────────
echo [INFO] Running setup (creates Platinum folders if missing)...
python setup\setup_platinum.py
echo.

REM ── Virtual environment ───────────────────────────────────────
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
    echo Installing dependencies...
    venv\Scripts\pip install -r requirements.txt
    echo.
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [INFO] Starting Local Orchestrator...
echo [INFO] Watching: Approved/ (approved actions to execute)
echo [INFO] Watching: Updates/ (cloud updates to merge into Dashboard)
echo [INFO] Press Ctrl+C to stop.
echo.

python local\local_orchestrator.py

pause
