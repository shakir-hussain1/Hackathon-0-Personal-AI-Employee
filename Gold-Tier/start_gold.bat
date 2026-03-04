@echo off
echo ========================================
echo   Gold Tier AI Employee Starting
echo ========================================
echo.

REM Run from Gold-Tier root
cd /d "%~dp0"

REM ── Pre-flight checks ───────────────────────────────────────────────────────
if not exist ".env" (
    if exist ".env.example" (
        echo [WARN] .env not found. Copying from .env.example...
        copy ".env.example" ".env" >nul
        echo [WARN] IMPORTANT: Edit .env before enabling live features!
        echo        - Set DRY_RUN=false only when all credentials are ready
        echo        - Add API keys for Facebook, Twitter, Odoo as needed
        echo.
    )
)

REM ── Docker check (Odoo) ──────────────────────────────────────────────────────
echo Checking Docker for Odoo...
docker ps >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Docker not running. Odoo features will be DISABLED.
    echo        To enable: Start Docker Desktop, then run:
    echo        docker-compose -f Gold-Tier\docker\docker-compose.odoo.yml up -d
    echo.
) else (
    echo [INFO] Docker running. Check Odoo: http://localhost:8069
    echo.
)

REM ── Virtual environment ─────────────────────────────────────────────────────
if not exist "venv\Scripts\activate.bat" (
    echo Creating Gold-Tier virtual environment...
    python -m venv venv
    echo Installing dependencies...
    venv\Scripts\pip install -r requirements.txt
    echo.
    echo [INFO] Installing Playwright browser (for WhatsApp)...
    venv\Scripts\playwright install chromium
    echo.
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

REM ── Memory check ────────────────────────────────────────────────────────────
echo.
echo [INFO] System memory check:
wmic OS get FreePhysicalMemory /value | find "="
echo [TIP]  For 8GB RAM: Keep DRY_RUN=true, run Gold + Silver (not both + Odoo simultaneously)
echo.

echo Starting Gold Tier Orchestrator...
echo Press Ctrl+C to stop.
echo.

python orchestrator\orchestrator.py

pause
