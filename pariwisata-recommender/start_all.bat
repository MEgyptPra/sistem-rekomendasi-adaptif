@echo off
echo ============================================================
echo    PARIWISATA RECOMMENDER - START ALL SERVICES
echo ============================================================
echo.

REM Get current directory
set ROOT_DIR=%~dp0

echo Step 1/5: Checking Docker Desktop...
docker ps 1>nul 2>nul
if %errorlevel% neq 0 (
    echo WARNING: Docker Desktop is not running. Starting...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    echo          Waiting for Docker Desktop to start 30 seconds...
    timeout /t 30 /nobreak 1>nul
    echo          Done waiting
)
echo SUCCESS: Docker Desktop is ready
echo.

echo Step 2/5: Starting PostgreSQL Database (Docker)...
cd /d "%ROOT_DIR%"
docker-compose up -d db
if %errorlevel% neq 0 (
    echo ERROR: Failed to start database. Make sure Docker Desktop is running.
    pause
    exit /b 1
)
echo SUCCESS: Database started successfully
echo.

echo Step 3/5: Starting Backend API Server (Port 8000)...
cd /d "%ROOT_DIR%backend"
start "Backend API Server" cmd /k "python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 3 /nobreak 1>nul
echo SUCCESS: Backend server started
echo.

echo Step 4/5: Starting Admin Dashboard (Port 3000)...
cd /d "%ROOT_DIR%admin-dashboard"
start "Admin Dashboard" cmd /k "npm start"
timeout /t 3 /nobreak 1>nul
echo SUCCESS: Admin dashboard started
echo.

echo Step 5/5: Starting Frontend Website (Port 5173)...
cd /d "%ROOT_DIR%frontend"
start "Frontend Website" cmd /k "npm run dev"
timeout /t 3 /nobreak 1>nul
echo SUCCESS: Frontend website started
echo.

echo ============================================================
echo    ALL SERVICES STARTED SUCCESSFULLY!
echo ============================================================
echo.
echo Backend API:       http://localhost:8000
echo API Docs:          http://localhost:8000/docs
echo Admin Dashboard:   http://localhost:3000 (Login: admin@example.com)
echo Frontend Website:  http://localhost:5173
echo.
echo Admin Login credentials:
echo   Email:    admin@example.com
echo   Password: admin123
echo.
echo Press any key to open Frontend Website in browser...
pause 1>nul
start http://localhost:5173
echo.
echo Services are running in separate windows.
echo Close those windows to stop the services.
echo.
pause
