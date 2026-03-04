@echo off
echo ========================================
echo   Bronze Tier AI Employee Starting
echo ========================================
echo.

REM Run from Bronze-Tier root regardless of launch location
cd /d "%~dp0"

REM ── Pre-flight: vault folder ──────────────────────────────────────────────────
if not exist "..\Common\AI_Employee_Vault\Inbox" (
    echo [WARN] Vault Inbox folder not found. Creating folder structure...
    mkdir "..\Common\AI_Employee_Vault\Inbox"      2>nul
    mkdir "..\Common\AI_Employee_Vault\Needs_Action" 2>nul
    mkdir "..\Common\AI_Employee_Vault\Done"        2>nul
    mkdir "..\Common\AI_Employee_Vault\Logs"        2>nul
    mkdir "..\Common\AI_Employee_Vault\Plans"       2>nul
    echo [OK] Vault folders created.
    echo.
) else (
    echo [OK] Vault folder exists.
)

REM ── Pre-flight: venv ─────────────────────────────────────────────────────────
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
echo [INFO] Vault: %~dp0..\Common\AI_Employee_Vault
echo [INFO] Drop files into Inbox\ to trigger the AI employee.
echo [INFO] Tasks appear in Needs_Action\, processed files go to Done\
echo.
echo Starting Bronze Tier File System Watcher...
echo Press Ctrl+C to stop.
echo.

python watchers\filesystem_watcher.py

pause
