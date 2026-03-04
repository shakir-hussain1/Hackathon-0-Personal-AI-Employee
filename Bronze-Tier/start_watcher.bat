@echo off
echo ============================================================
echo Starting AI Employee File System Watcher
echo ============================================================
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat
python watchers\filesystem_watcher.py

pause
