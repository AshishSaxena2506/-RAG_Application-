@echo off
title TASK 3 - MODEL INTEGRATION
setlocal

echo ============================================
echo        TASK 3 - MODEL INTEGRATION
echo ============================================

REM === 1) Go to THIS folder (where bat file exists) ===
cd /d "%~dp0"

REM === 2) Activate venv ===
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat
echo [OK] Virtual environment activated.
echo.

REM === 3) Ensure sentence-transformers installed ===
pip show sentence-transformers >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing sentence-transformers ...
    pip install sentence-transformers
) else (
    echo [OK] sentence-transformers already installed.
)
echo.

REM === 4) Check if Ollama is running ===
echo [INFO] Checking Ollama server on localhost:11434 ...
curl -s http://localhost:11434/api/tags >nul
if %errorlevel% neq 0 (
    echo [ERROR] Ollama NOT running!
    echo Please start Ollama manually and try again.
    pause
    exit /b 1
)
echo [OK] Ollama is running and responding.
echo.

REM === 5) Run chatbot ===
echo [INFO] Starting RAG chatbot (Ollama + LLaMA2) ...
python run_chat.py

echo.
echo ============================================
echo   TASK 3 Finished (Model Integration)
echo ============================================
pause
endlocal
