@echo off
echo ========================================
echo Restarting Backend Server
echo ========================================
echo.
echo Stopping any existing backend processes...

REM Kill any Python processes running uvicorn
taskkill /F /FI "WINDOWTITLE eq Backend API Server*" 2>nul

REM Kill any process using port 8000
echo Killing process on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    echo Killing PID %%a
    taskkill /F /PID %%a 2>nul
)

timeout /t 2 /nobreak >nul

echo.
echo Starting Backend API Server with auto-reload...
cd /d "%~dp0"

start "Backend API Server" cmd /k "python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo ========================================
echo Backend server restarted!
echo ========================================
echo.
echo Backend API:  http://localhost:8000
echo API Docs:     http://localhost:8000/docs
echo.
echo The server window will open in a new terminal.
echo Check that terminal for any errors.
echo.
pause
