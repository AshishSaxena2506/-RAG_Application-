@echo off
title TASK 6 - FINAL REPORT (PDF)
cd /d "%~dp0"

echo ============================================
echo        TASK 6 - FINAL REPORT (PDF)
echo ============================================

REM 1) Activate venv
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] .venv\Scripts\activate.bat not found.
    echo Run Task 0 / setup first.
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat
echo [OK] Virtual environment activated.
echo.

REM 2) Ensure reportlab is available
echo [INFO] Checking for reportlab ...
python -c "import reportlab" 2>nul
if errorlevel 1 (
    echo [INFO] reportlab not found. Installing...
    pip install reportlab
) else (
    echo [OK] reportlab already installed.
)
echo.

REM 3) Generate report\report.pdf
echo [INFO] Generating final report PDF from evaluation + config ...
python generate_report.py

if exist "report\report.pdf" (
    echo.
    echo [OK] report.pdf generated at: report\report.pdf
) else (
    echo.
    echo [ERROR] report\report.pdf was NOT created. Check generate_report.py.
)

echo.
echo ============================================
echo   TASK 6 Finished - Final PDF Report Ready
echo ============================================
pause >nul
