@echo off
title TASK 2 - VECTOR DATABASE
setlocal

echo ============================================
echo        TASK 2 - VECTOR DATABASE
echo ============================================
echo.

REM --- 1) Go to the folder where this BAT lives ---
cd /d "%~dp0"

REM --- 2) Activate virtual environment ---
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] .venv\Scripts\activate.bat not found.
    echo Make sure you created the virtual environment in this folder.
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat
echo [OK] Virtual environment activated.
echo.

REM --- 3) Ensure sentence-transformers is available ---
python -c "import sentence_transformers" >nul 2>&1
if errorlevel 1 (
    echo [INFO] sentence-transformers not found, installing...
    pip install sentence-transformers --quiet
    if errorlevel 1 (
        echo [ERROR] Failed to install sentence-transformers.
        pause
        exit /b 1
    )
) else (
    echo [OK] sentence-transformers already installed.
)
echo.

REM --- 4) Build the vector database using vector_store.py ---
echo [INFO] Building FAISS vector index from chunks.pkl ...
python vector_store.py
if errorlevel 1 (
    echo.
    echo [ERROR] Task 2 FAILED!
    pause
    exit /b 1
)

echo.
echo ============================================
echo   TASK 2 Completed Successfully!
echo   Vector DB stored under artifacts\faiss_index
echo ============================================

echo.
echo Press any key to close this window.
pause >nul
endlocal
