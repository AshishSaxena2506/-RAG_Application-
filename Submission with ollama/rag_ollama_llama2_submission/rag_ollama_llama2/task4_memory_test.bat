@echo off
title TASK 4 - CONVERSATIONAL MEMORY
cd /d "%~dp0"

echo ============================================
echo        TASK 4 - CONVERSATIONAL MEMORY
echo ============================================

REM 1) Activate venv
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] .venv\Scripts\activate.bat not found.
    echo Run Task 0/README setup first.
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat
echo [OK] Virtual environment activated.
echo.

REM 2) Brief instructions
echo This will run an automatic 3-turn conversation:
echo   Turn 1: My name is Ashish, remember this.
echo   Turn 2: What is self-attention in Transformers?
echo   Turn 3: And what is my name?
echo.
echo Output below should show that in Turn 3 the bot
echo correctly answers that your name is "Ashish".
echo.

REM 3) Run the memory test script
python memory_test.py

echo.
echo ============================================
echo   TASK 4 Completed - Conversational Memory Test
echo   Take a screenshot of the 3 turns for the report.
echo ============================================
pause >nul
