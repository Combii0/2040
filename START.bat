@echo off
setlocal
cd /d "%~dp0"

title RoboYork 2040 - Launcher

echo ==========================================
echo          ROBOYORK 2040 - STARTER
echo ==========================================
echo.

set "PYTHON_CMD="

py -3 -c "import sys; print(sys.version)" >nul 2>nul
if %errorlevel%==0 (
    set "PYTHON_CMD=py -3"
    goto :python_ready
)

python -c "import sys; print(sys.version)" >nul 2>nul
if %errorlevel%==0 (
    set "PYTHON_CMD=python"
    goto :python_ready
)

echo Python 3 was not found.
echo.

where winget >nul 2>nul
if %errorlevel%==0 (
    echo Trying to install Python 3 automatically with winget...
    echo.

    winget install --id Python.Python.3.14 -e ^
        --accept-package-agreements ^
        --accept-source-agreements

    echo.
    echo Checking Python again...

    py -3 -c "import sys" >nul 2>nul
    if %errorlevel%==0 (
        set "PYTHON_CMD=py -3"
        goto :python_ready
    )

    python -c "import sys" >nul 2>nul
    if %errorlevel%==0 (
        set "PYTHON_CMD=python"
        goto :python_ready
    )

    echo.
    echo Python may have been installed, but Windows has not refreshed PATH yet.
    echo Close this window and run START.bat again.
    echo.
    pause
    exit /b 1
)

echo winget is not available on this computer.
echo Opening the official Python download page...
start "" "https://www.python.org/downloads/windows/"
echo.
echo Install Python 3, enable "Add python.exe to PATH",
echo keep Tcl/Tk enabled, and then run START.bat again.
echo.
pause
exit /b 1


:python_ready
echo Python found.
echo.

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv .venv

    if errorlevel 1 (
        echo.
        echo ERROR: The virtual environment could not be created.
        echo Try reinstalling Python from python.org with pip and venv enabled.
        echo.
        pause
        exit /b 1
    )
)

set "VENV_PY=.venv\Scripts\python.exe"

echo Checking pip...
"%VENV_PY%" -m ensurepip --upgrade >nul 2>nul
"%VENV_PY%" -m pip install --upgrade pip setuptools wheel

if errorlevel 1 (
    echo.
    echo ERROR: pip could not be prepared.
    echo.
    pause
    exit /b 1
)

echo.
echo Checking pygame...
"%VENV_PY%" -c "import pygame" >nul 2>nul

if errorlevel 1 (
    echo Installing pygame...
    "%VENV_PY%" -m pip install pygame

    if errorlevel 1 (
        echo.
        echo ERROR: pygame could not be installed.
        echo Check the Internet connection and run START.bat again.
        echo.
        pause
        exit /b 1
    )
) else (
    echo pygame is already installed.
)

echo.
echo Checking Tkinter...
"%VENV_PY%" -c "import tkinter; print('Tkinter OK')" >nul 2>nul

if errorlevel 1 (
    echo.
    echo ERROR: Tkinter is not available.
    echo Reinstall Python from python.org and keep Tcl/Tk enabled.
    echo Opening the official Python page...
    start "" "https://www.python.org/downloads/windows/"
    echo.
    pause
    exit /b 1
)

echo.
echo All checks passed.
echo Starting RoboYork 2040...
echo.

"%VENV_PY%" main.py
set "GAME_EXIT=%errorlevel%"

if not "%GAME_EXIT%"=="0" (
    echo.
    echo RoboYork closed with error code %GAME_EXIT%.
    echo Review the messages above.
    echo.
    pause
)

exit /b %GAME_EXIT%
