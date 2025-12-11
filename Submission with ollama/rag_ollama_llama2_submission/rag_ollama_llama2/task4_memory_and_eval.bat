@echo off
title TASK 4_5 - MEMORY_EVALUATION
cd /d "%~dp0"

echo ============================================
echo    TASK 4 - CONVERSATIONAL MEMORY TEST
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

REM 2) Brief instructions for memory test
echo This will run an automatic 3-turn conversation:
echo   Turn 1: My name is Ashish, remember this.
echo   Turn 2: What is self-attention in Transformers?
echo   Turn 3: And what is my name?
echo.
echo Output below should show that in Turn 3 the bot
echo correctly answers that your name is "Ashish".
echo.

REM 3) Run the memory test script (Task 4)
python memory_test.py
if errorlevel 1 (
    echo.
    echo [ERROR] memory_test.py failed. Check traceback above.
    goto END
)

echo.
echo ============================================
echo   TASK 4 Completed - Conversational Memory OK
echo   Take a screenshot of the 3 turns for the report.
echo ============================================
echo.

REM ===========================================
REM ==========  TASK 5 - EVALUATION  ==========
REM ===========================================

echo ============================================
echo        TASK 5 - 10 Qn RAGAS EVALUATION
echo ============================================
echo [INFO] Running 10-question evaluation with RAGAS...
echo.

REM Check that questions.json exists
if not exist "questions.json" (
    echo [ERROR] questions.json not found in %CD%.
    echo Make sure questions.json is in the rag_ollama_llama2 folder.
    goto END
)

REM Run evaluation.py (uses RAGBot + FAISS index + Ollama)
python evaluation.py
if errorlevel 1 (
    echo.
    echo [ERROR] evaluation.py failed. See error above.
    goto END
)

echo.
echo [OK] Evaluation completed.
if exist "artifacts\eval_results.json" (
    echo Results saved to: artifacts\eval_results.json
) else (
    echo [WARN] eval_results.json not found. Check evaluation.py.
)

:END
echo.
echo ============================================
echo   TASK 4_5 Finished
echo   - Task 4: Memory behaviour tested
echo   - Task 5: RAGAS evaluation run
echo ============================================
pause >nul
