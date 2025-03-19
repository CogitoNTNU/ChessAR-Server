#!/bin/bash

if command -v python3 &>/dev/null; then
    echo "Python 3 is installed."
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    echo "Python is installed."
    PYTHON_CMD="python"
else
    echo "Python is not installed. Please install Python and try again."
    exit 1
fi

OS="$(uname -s)"

if [[ "$OS" == "Darwin"* ]]; then
    echo "Installing requirements using pip3..."
    pip3 install -r requirements.txt
else
    echo "Installing requirements using pip..."
    pip install -r requirements.txt
fi

echo "Running tests with pytest..."
pytest
