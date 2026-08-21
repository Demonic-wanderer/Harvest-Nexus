@echo off
setlocal
set "ROOT=%~dp0"
echo ===================================================
echo     STARTING HARVEST NEXUS CLOUD PLATFORM
echo ===================================================

:: 1. Start Cloud Backend (Forge)
start "Forge Backend (Port 5000)" cmd /k "npm run dev"

:: 2. Start Oracle AI Engine
start "Oracle AI (Port 8001)" cmd /k "cd /d ""%ROOT%AI Engines"" && uvicorn oracle_api:app --port 8001 --reload"

:: 3. Start Insight Market Module
start "Insight Market (Port 8000)" cmd /k "cd insight_module_final && uvicorn app.main:app --port 8000 --reload"

echo All backend microservices launched successfully!
echo Launching Flutter App...
cd /d "%ROOT%frontend\flutter_application_1_ui"
flutter run -d chrome
