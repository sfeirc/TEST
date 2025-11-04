@echo off
echo ========================================
echo   Infotel RFP Summarizer Backend
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found!
    echo.
    echo Please create a .env file with your API keys.
    echo You can copy env_template.txt to .env and edit it.
    echo.
    pause
    exit /b 1
)

echo Starting server on http://localhost:3001...
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python main.py

pause

