@echo off
cd /d %~dp0

REM Add all files
git add .

REM Commit with timestamp-based message
for /f %%i in ('powershell -command "Get-Date -Format yyyy-MM-dd_HH-mm-ss"') do set timestamp=%%i
git commit -m "🧠 Auto-push from Uriel V6 at %timestamp%" >nul 2>&1

REM Push to GitHub
git push -u origin main

REM Done
echo ✅ Auto-push complete at %timestamp%
pause
