#!/bin/bash

set -e

echo "Cloning repository..."
git clone https://github.com/yehorscode/RssTUI RssTUI
cd RssTUI

echo """

██████╗ ███████╗███████╗████████╗██╗   ██╗██╗
██╔══██╗██╔════╝██╔════╝╚══██╔══╝██║   ██║██║
██████╔╝███████╗███████╗   ██║   ██║   ██║██║
██╔══██╗╚════██║╚════██║   ██║   ██║   ██║██║
██║  ██║███████║███████║   ██║   ╚██████╔╝██║
╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝

"""

echo "Setting Python version..."
if command -v pyenv >/dev/null 2>&1; then
    pyenv shell 3.11.4 || echo "Warning: Could not set pyenv to 3.11.4, this isn't a crucial bug"
fi

echo "Activating virtual environment..."
if [ -n "$FISH_VERSION" ]; then
    source venv/bin/activate.fish
elif [ -n "$ZSH_VERSION" ]; then
    source venv/bin/activate
elif [ -n "$BASH_VERSION" ]; then
    source venv/bin/activate
else
    source venv/bin/activate 2>/dev/null || \
    source venv/bin/activate.fish 2>/dev/null || \
    source venv/bin/activate.csh 2>/dev/null || \
    { echo "Error: Could not activate virtual environment"; exit 1; }
fi

echo "Installing requirements..."
pip install -r requirements.txt

echo """



INSTALLED!!! PLEASE RUN THIS:

cd RssTUI && source venv/bin/activate && python3 app.py

okay???
"""
