@echo off
echo ============================================================
echo    CLEANUP UNUSED FILES - SCAN RESULTS
echo ============================================================
echo.
echo File yang TIDAK DIPAKAI dan akan dihapus:
echo.
echo [BACKEND FOLDER]
echo   1. backend\setup_database.py          (diganti start_all.bat)
echo   2. backend\test_admin_login.py        (file test manual)
echo   3. backend\test_login.py              (file test manual)
echo   4. backend\start_backend.bat          (diganti start_all.bat)
echo.
echo [ROOT FOLDER]
echo   5. setup_docker_db.bat                (diganti start_all.bat)
echo   6. cleanup_unused_files.bat           (versi lama)
echo.
echo [DOKUMENTASI - Opsional]
echo   7. DATABASE_SETUP.md                  (sudah ada QUICK_START.md)
echo   8. DOCKER_DATABASE_SETUP.md           (sudah ada QUICK_START.md)
echo   9. TROUBLESHOOTING_DATABASE.md        (sudah ada QUICK_START.md)
echo  10. TROUBLESHOOTING_LOGIN.md           (sudah ada QUICK_START.md)
echo  11. ADMIN_LOGIN.md                     (sudah ada QUICK_START.md)
echo.
echo ============================================================
echo.
echo Apakah Anda yakin ingin menghapus file-file ini?
echo (Dokumentasi .md akan tetap ada sebagai backup)
echo.
set /p CONFIRM="Ketik YES untuk menghapus file unused: "
if /i not "%CONFIRM%"=="YES" (
    echo.
    echo Dibatalkan. Tidak ada file yang dihapus.
    pause
    exit /b 0
)

echo.
echo ============================================================
echo    MEMULAI CLEANUP...
echo ============================================================
echo.

REM Pindah ke directory script
cd /d "%~dp0"

REM Delete backend test files
echo [1/6] Menghapus backend\setup_database.py...
if exist "backend\setup_database.py" (
    del /Q "backend\setup_database.py"
    echo   ✓ Terhapus
) else (
    echo   - Sudah tidak ada
)

echo [2/6] Menghapus backend\test_admin_login.py...
if exist "backend\test_admin_login.py" (
    del /Q "backend\test_admin_login.py"
    echo   ✓ Terhapus
) else (
    echo   - Sudah tidak ada
)

echo [3/6] Menghapus backend\test_login.py...
if exist "backend\test_login.py" (
    del /Q "backend\test_login.py"
    echo   ✓ Terhapus
) else (
    echo   - Sudah tidak ada
)

echo [4/6] Menghapus backend\start_backend.bat...
if exist "backend\start_backend.bat" (
    del /Q "backend\start_backend.bat"
    echo   ✓ Terhapus
) else (
    echo   - Sudah tidak ada
)

echo [5/6] Menghapus setup_docker_db.bat...
if exist "setup_docker_db.bat" (
    del /Q "setup_docker_db.bat"
    echo   ✓ Terhapus
) else (
    echo   - Sudah tidak ada
)

echo [6/6] Menghapus cleanup_unused_files.bat (versi lama)...
if exist "cleanup_unused_files.bat" (
    del /Q "cleanup_unused_files.bat"
    echo   ✓ Terhapus
) else (
    echo   - Sudah tidak ada
)

echo.
echo ============================================================
echo    CLEANUP SELESAI!
echo ============================================================
echo.
echo File yang MASIH ADA (essential):
echo   ✓ start_all.bat             (startup semua services)
echo   ✓ stop_all.bat              (stop semua services)
echo   ✓ force_stop_all.bat        (emergency stop)
echo   ✓ docker-compose.yml        (database config)
echo   ✓ backend\main.py           (backend main)
echo   ✓ backend\admin_routes.py   (admin API)
echo   ✓ backend\.env              (database config)
echo   ✓ backend\requirements.txt  (dependencies)
echo   ✓ backend\app\              (core application)
echo   ✓ admin-dashboard\          (admin UI)
echo   ✓ frontend\                 (user frontend)
echo   ✓ README.md                 (main docs)
echo   ✓ QUICK_START.md            (quick start guide)
echo.
echo Dokumentasi lama tetap ada sebagai referensi:
echo   - DATABASE_SETUP.md
echo   - DOCKER_DATABASE_SETUP.md
echo   - TROUBLESHOOTING_DATABASE.md
echo   - TROUBLESHOOTING_LOGIN.md
echo   - ADMIN_LOGIN.md
echo.
echo Jika ingin hapus dokumentasi lama, hapus manual saja.
echo.
pause
