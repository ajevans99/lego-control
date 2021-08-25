#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "Moving to directory ${SCRIPT_DIR}"
cd $SCRIPT_DIR

source venv/bin/activate

if pip install -r requirements.txt; then
    echo "Installed requirements with pip"
else
    echo "Failed to install requirements with pip"
fi

if python main.py; then
    echo "Main.py finished with exit code 0"
else
    echo "Main.py finished with non-zero exit code"
fi
