@echo off
title TASK 1 - PDF Ingestion (RAG Assignment)
setlocal

echo ============================================
echo      TASK 1 - PDF INGESTION PIPELINE
echo ============================================
echo.

REM === 1) Move to folder where this BAT exists ===
cd /d "%~dp0"

REM === 2) Activate virtual environment ===
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    pause
    exit /b 1
)
call .venv\Scripts\activate.bat

echo [OK] Virtual environment activated.
echo.

REM === 3) Run ingestion pipeline ===
echo Running PDF ingestion...
python ingest.py

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] ingest.py failed!!
    pause
    exit /b 1
)

echo.
echo ============================================
echo   TASK 1 Completed Successfully!
echo   PDFs ingested + chunked + embedded.
echo ============================================
echo.

pause
endlocal
