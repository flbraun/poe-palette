#!/bin/bash

LEAGUE_TYPE=$1

cd /app
source /etc/env/poepalettedata/loadenv.sh
python3 -m poepalettedata $LEAGUE_TYPE
