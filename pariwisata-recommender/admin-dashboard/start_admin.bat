@echo off
echo ========================================
echo Starting Admin Dashboard
echo ========================================
echo.

cd /d "%~dp0"

:: Check if node_modules exists
if not exist "node_modules\" (
    echo Installing dependencies...
    call npm install
    echo.
)

:: Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Creating default .env file...
    (
        echo # Admin Dashboard Environment Variables
        echo REACT_APP_API_URL=http://localhost:8000
        echo REACT_APP_ADMIN_URL=http://localhost:3000
        echo.
        echo # Port configuration (default 3000)
        echo # PORT=3000
    ) > .env
    echo .env file created!
    echo.
)

echo.
echo ========================================
echo Starting React Development Server
echo ========================================
echo Admin Dashboard will open at: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

:: Start the development server
call npm start

pause
