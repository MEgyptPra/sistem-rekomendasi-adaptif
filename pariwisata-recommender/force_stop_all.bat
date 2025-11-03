@echo off
echo ============================================================
echo    FORCE STOP ALL SERVICES (Emergency)
echo ============================================================
echo.
echo WARNING: This will force close everything!
echo Press Ctrl+C to cancel, or
pause

echo.
echo [1/4] Killing Backend (Port 8000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000"') do taskkill /F /PID %%a 2>nul
echo Done.

echo [2/4] Killing Admin Dashboard (Port 3000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":3000"') do taskkill /F /PID %%a 2>nul
echo Done.

echo [3/4] Killing Docker Containers...
for /f %%i in ('docker ps -q') do docker kill %%i 2>nul
echo Done.

echo [4/4] Killing Docker Desktop...
taskkill /F /IM "Docker Desktop.exe" 2>nul
taskkill /F /IM "com.docker.backend.exe" 2>nul
taskkill /F /IM "com.docker.proxy.exe" 2>nul
echo Done.

echo.
echo ============================================================
echo    FORCE STOP COMPLETE
echo ============================================================
echo.
echo All processes have been forcefully terminated.
echo You can now restart services with start_all.bat
echo.
pause
