@echo off
title RAG + OLLAMA + LLAMA2 BOT
setlocal

REM Go to this folder
cd /d "%~dp0"

REM Activate venv in THIS folder
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] venv not found at .venv\Scripts\activate.bat
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat

echo ============================================
echo   RAG + OLLAMA + LLAMA2 BOT
echo ============================================
echo Virtual environment activated.
echo.

if not exist "run_chat.py" (
    echo [ERROR] run_chat.py not found in %CD%
    pause
    exit /b 1
)

python run_chat.py

echo.
echo Chatbot finished. Press any key to close this window.
pause >nul
endlocal
