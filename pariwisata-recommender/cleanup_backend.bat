@echo off
REM Cleanup unused, debug, and documentation files in backend

echo =============================================
echo   CLEANUP UNUSED & DEBUG FILES (BACKEND)
echo =============================================

REM Documentation & markdown files
DEL /Q "backend\CONTEXT_AWARE_COMPONENTS.md"
DEL /Q "backend\CONTEXT_COMPATIBILITY.md"
DEL /Q "backend\FRONTEND_API_DOCS.md"
DEL /Q "backend\INCREMENTAL_LEARNING_GUIDE.md"
DEL /Q "backend\KONFIRMASI_CONTEXT_AWARE.md"
DEL /Q "backend\LOW_PRIORITY_API_DOCS.md"
DEL /Q "backend\MEDIUM_PRIORITY_API_DOCS.md"
DEL /Q "backend\QUICKSTART_REALTIME_API.md"
DEL /Q "backend\REALTIME_DATA_SETUP.md"
DEL /Q "backend\REALTIME_INTEGRATION_COMPLETE.md"
DEL /Q "backend\VERIFIKASI_AKHIR_CONTEXT.md"

REM Debug & batch files
DEL /Q "backend\restart_backend.bat"

REM Once-off scripts
DEL /Q "backend\fix_user_sequence.py"
DEL /Q "backend\check_activities.py"
DEL /Q "backend\check_database_destinations.py"
DEL /Q "backend\check_model_status.py"
DEL /Q "backend\check_realtime_api.py"
DEL /Q "backend\migrate_db.py"
DEL /Q "backend\migrate_medium_priority.py"
DEL /Q "backend\migrate_realtime_api_config.py"
DEL /Q "backend\seed_activities.py"
DEL /Q "backend\seed_realtime_api_config.py"

echo Backend cleanup complete.
pause
