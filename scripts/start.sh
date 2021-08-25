#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "Moving to directory ${SCRIPT_DIR}"
cd $SCRIPT_DIR

git pull

# Run API

docker run -p 6379:6379 -d redis:5

source ../server/venv/bin/activate
pip install -r ../server/requirements.txt


# Run webserver
cd ../client_web
{ yarn start; python ../server/manage.py runserver; } &

# Open Chrome in Kiosk mode

export DISPLAY=:0
chromium-browser --noerrdialogs --kiosk localhost:3000
