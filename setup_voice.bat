@echo off
REM Setup script for VPET voice features on Windows

echo.
echo ========================================
echo   VPET Voice Feature Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from python.org
    pause
    exit /b 1
)

echo Python found: 
python --version
echo.

echo Installing voice interaction dependencies...
echo.

REM Install required packages
python -m pip install --upgrade pip setuptools wheel
echo.
python -m pip install SpeechRecognition pynput edge-tts

if errorlevel 1 (
    echo.
    echo WARNING: Some packages failed to install
    echo You may need to:
    echo   1. Run as Administrator
    echo   2. Check internet connection
    echo   3. Update Python
    echo.
    pause
) else (
    echo.
    echo ========================================
    echo   Installation Complete!
    echo ========================================
    echo.
    echo Voice feature is now ready to use:
    echo   - Press Alt+V and hold to speak
    echo   - Release to send
    echo   - Pet responds in Japanese voice
    echo.
    echo For more info, see VOICE_FEATURE.md
    echo.
    pause
)
