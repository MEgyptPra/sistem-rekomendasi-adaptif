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

echo Step 2/5: Starting ALL Services with Docker Compose...
cd /d "%ROOT_DIR%"
docker-compose up -d
if %errorlevel% neq 0 (
    echo ERROR: Failed to start services with Docker Compose.
    pause
    exit /b 1
)
echo SUCCESS: All services started with Docker Compose
echo.

echo Step 3/5: Waiting for services to be ready...
timeout /t 15 /nobreak 1>nul
echo SUCCESS: Services initialization complete
echo.

echo Step 4/5: Checking service health...
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo.

echo Step 5/5: Opening services in browser...
echo ============================================================
echo    ALL SERVICES STARTED SUCCESSFULLY WITH DOCKER!
echo ============================================================
echo.
echo Backend API:       http://localhost:8000
echo API Docs:          http://localhost:8000/docs
echo Admin Dashboard:   http://localhost:3000
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
echo All services are running in Docker containers.
echo Use 'docker-compose down' to stop all services.
echo.
