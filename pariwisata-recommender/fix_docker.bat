@echo off
echo ============================================================
echo    FIX DOCKER DESKTOP ISSUES
echo ============================================================
echo.
echo This script will:
echo   1. Stop all Docker containers
echo   2. Restart Docker Desktop
echo   3. Wait for it to be ready
echo.
pause

echo.
echo [1/4] Stopping all application services first...
call "%~dp0stop_all.bat"

echo.
echo [2/4] Force stopping Docker Desktop...
taskkill /F /IM "Docker Desktop.exe" 2>nul
taskkill /F /IM "com.docker.backend.exe" 2>nul
taskkill /F /IM "com.docker.proxy.exe" 2>nul
timeout /t 3 /nobreak >nul
echo ✓ Docker Desktop stopped

echo.
echo [3/4] Starting Docker Desktop...
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
echo   Waiting for Docker Desktop to initialize (45 seconds)...
timeout /t 45 /nobreak >nul

echo.
echo [4/4] Verifying Docker is ready...
docker ps >nul 2>&1
if errorlevel 1 (
    echo ! Docker is still not ready. Please wait a bit more.
    echo   Check Docker Desktop icon in system tray.
) else (
    echo ✓ Docker Desktop is ready!
)

echo.
echo ============================================================
echo    FIX COMPLETED
echo ============================================================
echo.
echo You can now run start_all.bat
echo.
pause
