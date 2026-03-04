@echo off
echo ============================================================
echo   Personal AI Employee - All Tiers Starting
echo ============================================================
echo.

cd /d "%~dp0"

echo [1/3] Starting Bronze Tier (File System Watcher)...
start "Bronze Tier - File Watcher" cmd /k "cd /d "%~dp0Bronze-Tier" && start_bronze.bat"
timeout /t 2 /nobreak >nul

echo [2/3] Starting Silver Tier (Gmail + Calendar + LinkedIn)...
start "Silver Tier - Orchestrator" cmd /k "cd /d "%~dp0Silver-Tier" && start_silver.bat"
timeout /t 2 /nobreak >nul

echo [3/3] Starting Gold Tier (Odoo + Social Media + CEO Briefing)...
start "Gold Tier - Orchestrator" cmd /k "cd /d "%~dp0Gold-Tier" && start_gold.bat"
timeout /t 2 /nobreak >nul

echo.
echo ============================================================
echo   All 3 Tiers launched in separate windows!
echo.
echo   Bronze: File watcher — drop files in Inbox\
echo   Silver: Gmail + Calendar + LinkedIn (needs credentials.json)
echo   Gold:   Odoo + Social Media + CEO Briefing (DRY_RUN=true)
echo.
echo   To stop any tier: Close its window or press Ctrl+C in it.
echo ============================================================
echo.
pause
