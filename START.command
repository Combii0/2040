#!/bin/bash

cd "$(dirname "$0")" || exit 1

echo "=========================================="
echo "         ROBOYORK 2040 - STARTER"
echo "=========================================="
echo ""

PYTHON_CMD=""

if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="$(command -v python3)"
fi

if [ -z "$PYTHON_CMD" ]; then
    echo "Python 3 was not found."
    echo ""

    if command -v brew >/dev/null 2>&1; then
        echo "Homebrew detected."
        echo "Trying to install Python automatically..."
        echo ""

        brew install python

        if command -v python3 >/dev/null 2>&1; then
            PYTHON_CMD="$(command -v python3)"
        fi
    fi
fi

if [ -z "$PYTHON_CMD" ]; then
    echo "Python could not be installed automatically."
    echo "Opening the official Python download page..."
    open "https://www.python.org/downloads/macos/" 2>/dev/null
    echo ""
    echo "Install Python 3 and run START.command again."
    echo ""
    read -r -p "Press Enter to close..."
    exit 1
fi

echo "Python found:"
"$PYTHON_CMD" --version
echo ""

if [ ! -x ".venv/bin/python" ]; then
    echo "Creating virtual environment..."
    "$PYTHON_CMD" -m venv .venv

    if [ $? -ne 0 ]; then
        echo ""
        echo "ERROR: The virtual environment could not be created."
        echo "Reinstall Python from python.org and run this launcher again."
        echo ""
        read -r -p "Press Enter to close..."
        exit 1
    fi
fi

VENV_PY=".venv/bin/python"

echo "Checking pip..."
"$VENV_PY" -m ensurepip --upgrade >/dev/null 2>&1
"$VENV_PY" -m pip install --upgrade pip setuptools wheel

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: pip could not be prepared."
    echo ""
    read -r -p "Press Enter to close..."
    exit 1
fi

echo ""
echo "Checking pygame..."

if ! "$VENV_PY" -c "import pygame" >/dev/null 2>&1; then
    echo "Installing pygame..."
    "$VENV_PY" -m pip install pygame

    if [ $? -ne 0 ]; then
        echo ""
        echo "ERROR: pygame could not be installed."
        echo "Check the Internet connection and run START.command again."
        echo ""
        read -r -p "Press Enter to close..."
        exit 1
    fi
else
    echo "pygame is already installed."
fi

echo ""
echo "Checking Tkinter..."

if ! "$VENV_PY" -c "import tkinter" >/dev/null 2>&1; then
    echo "Tkinter was not found."

    if command -v brew >/dev/null 2>&1; then
        PY_MINOR="$("$PYTHON_CMD" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"

        echo "Trying to install the matching Homebrew Tk package..."
        brew install "python-tk@$PY_MINOR" >/dev/null 2>&1 || true
    fi
fi

if ! "$VENV_PY" -c "import tkinter" >/dev/null 2>&1; then
    echo ""
    echo "ERROR: Tkinter is not available."
    echo "Install Python from python.org, which normally includes Tcl/Tk:"
    echo "https://www.python.org/downloads/macos/"
    open "https://www.python.org/downloads/macos/" 2>/dev/null
    echo ""
    read -r -p "Press Enter to close..."
    exit 1
fi

echo ""
echo "All checks passed."
echo "Starting RoboYork 2040..."
echo ""

"$VENV_PY" main.py
GAME_EXIT=$?

if [ $GAME_EXIT -ne 0 ]; then
    echo ""
    echo "RoboYork closed with error code $GAME_EXIT."
    echo "Review the messages above."
    echo ""
    read -r -p "Press Enter to close..."
fi

exit $GAME_EXIT
