@echo off
echo ============================================================
echo    PARIWISATA RECOMMENDER - STOP ALL SERVICES
============================================================
echo.

echo Step 1/4: Stopping Backend API Server (Port 8000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a 2>nul
    if %errorlevel% equ 0 echo SUCCESS: Backend server stopped
)
echo.

echo Step 2/4: Stopping Admin Dashboard (Port 3000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":3000" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a 2>nul
    if %errorlevel% equ 0 echo SUCCESS: Admin dashboard stopped
)
echo.

echo Step 3/4: Stopping Frontend Website (Port 5173)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5173" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a 2>nul
    if %errorlevel% equ 0 echo SUCCESS: Frontend website stopped
)
echo.

echo Step 4/4: Stopping Database Container...
cd /d "%~dp0"

REM Method 1: Try docker-compose down
echo   Trying docker-compose down...
docker-compose down 2>nul
if %errorlevel% equ 0 (
    echo SUCCESS: Database stopped via docker-compose
    goto done
)

REM Method 2: If docker-compose fails, try docker stop directly
echo   docker-compose failed, trying direct docker stop...
docker stop pariwisata-recommender-db-1 2>nul
if %errorlevel% equ 0 (
    echo SUCCESS: Database stopped via docker stop
    goto done
)

REM Method 3: If both fail, kill Docker Desktop
echo   Docker commands not responding, trying to stop via Docker Desktop...
taskkill /F /IM "Docker Desktop.exe" 2>nul
if %errorlevel% equ 0 (
    echo SUCCESS: Docker Desktop closed (database stopped)
) else (
    echo WARNING: Could not stop database - please close Docker Desktop manually
)

:done
echo.
echo ============================================================
echo    ALL SERVICES STOPPED
echo ============================================================
echo.
echo Note: If you see errors above, services might already be stopped.
echo.
pause
