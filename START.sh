#!/bin/bash

cd "$(dirname "$0")" || exit 1

echo "=========================================="
echo "         ROBOYORK 2040 - STARTER"
echo "=========================================="
echo ""

install_linux_python() {
    if command -v apt >/dev/null 2>&1; then
        echo "apt detected."
        sudo apt update
        sudo apt install -y python3 python3-pip python3-venv python3-tk
        return $?
    fi

    if command -v dnf >/dev/null 2>&1; then
        echo "dnf detected."
        sudo dnf install -y python3 python3-pip python3-tkinter
        return $?
    fi

    if command -v pacman >/dev/null 2>&1; then
        echo "pacman detected."
        sudo pacman -Sy --needed --noconfirm python python-pip tk
        return $?
    fi

    if command -v zypper >/dev/null 2>&1; then
        echo "zypper detected."
        sudo zypper --non-interactive install python3 python3-pip python3-tk
        return $?
    fi

    return 1
}

if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 was not found."
    echo "Trying to install it with the detected package manager..."
    echo ""

    install_linux_python

    if ! command -v python3 >/dev/null 2>&1; then
        echo ""
        echo "ERROR: Python 3 could not be installed automatically."
        echo "Install Python 3, pip, venv and Tkinter for your distribution,"
        echo "then run START.sh again."
        echo ""
        exit 1
    fi
fi

PYTHON_CMD="$(command -v python3)"

echo "Python found:"
"$PYTHON_CMD" --version
echo ""

if ! "$PYTHON_CMD" -c "import tkinter" >/dev/null 2>&1; then
    echo "Tkinter is missing."
    echo "Trying to install the required system package..."
    install_linux_python
fi

if [ ! -x ".venv/bin/python" ]; then
    echo "Creating virtual environment..."
    "$PYTHON_CMD" -m venv .venv

    if [ $? -ne 0 ]; then
        echo ""
        echo "The virtual environment could not be created."
        echo "Trying to install the required system packages..."
        install_linux_python
        "$PYTHON_CMD" -m venv .venv
    fi
fi

if [ ! -x ".venv/bin/python" ]; then
    echo ""
    echo "ERROR: .venv could not be created."
    echo ""
    exit 1
fi

VENV_PY=".venv/bin/python"

echo "Checking pip..."
"$VENV_PY" -m ensurepip --upgrade >/dev/null 2>&1
"$VENV_PY" -m pip install --upgrade pip setuptools wheel

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: pip could not be prepared."
    echo ""
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
        echo "Check your Internet connection and system packages."
        echo ""
        exit 1
    fi
else
    echo "pygame is already installed."
fi

echo ""
echo "Checking Tkinter..."

if ! "$VENV_PY" -c "import tkinter" >/dev/null 2>&1; then
    echo ""
    echo "ERROR: Tkinter is not available."
    echo "Install the Tkinter package for your Linux distribution."
    echo ""
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
fi

exit $GAME_EXIT
