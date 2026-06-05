@echo off
REM Smart Parking System - Complete Startup Script
REM This script starts both the Bridge (Flask server) and Scanner (OpenCV/EasyOCR)

title Smart Parking System - Bridge & Scanner
color 0A

cls
echo.
echo ========================================================
echo   SMART PARKING SYSTEM - AUTO STARTUP
echo ========================================================
echo.
echo Checking Python installation...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from python.org
    pause
    exit /b
)

echo [OK] Python found
echo.
echo Starting components...
echo.

REM Start Bridge in a new window
echo [1/2] Starting Bridge (Flask Server) on localhost:5000...
start "Smart Parking Bridge" cmd /k python "Bridge_Updated.py"

REM Wait for Bridge to start
timeout /t 3 /nobreak

REM Start Scanner in another window
echo [2/2] Starting Camera Scanner (EasyOCR)...
start "Smart Parking Scanner" cmd /k python "BridgeCode_FIrebase_&_Gate(webcam OCR - Firebase auth check - entry push).py"

echo.
echo ========================================================
echo All services started!
echo.
echo Services running:
echo  • Bridge:  http://localhost:5000
echo  • Scanner: Webcam detection active
echo.
echo Keep this window open. Press Ctrl+C in any window to stop.
echo ========================================================
echo.
pause
