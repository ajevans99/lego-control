#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "Moving to directory ${SCRIPT_DIR}"
cd $SCRIPT_DIR

if git pull; then
    echo "Successfully pulled repo"
else
    echo "Failed to pull repo"
fi

# Run API

if /home/pi/redis/src/redis-server &>/dev/null & disown; then
    echo "Successfully ran docker with redis"
else
    echo "Failed to run docker with redis"
fi

source ../server/venv/bin/activate

if pip install -r ../server/requirements.txt; then
    echo "Dependencies updated"
fi
python ../server/manage.py runserver 0.0.0.0:8000 &>/dev/null & disown

# Run webserver
cd ../client_web
echo "Start API and client web servers"
yarn start &>/dev/null & disown

# Open Chrome in Kiosk mode

echo "Running Chromium in Kiosk mode"
export DISPLAY=:0
chromium-browser --noerrdialogs --kiosk localhost:3000

wait

# lsof -t -i tcp:3000 | xargs kill & lsof -t -i tcp:8000 | xargs kill
# Possibly useful: ./.config/lxsession/LXDE-pi/autostart
