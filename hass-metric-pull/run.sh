#!/bin/sh


export HASS_BEARERTOKEN="XXXXX"
export HASS_URL="http://XXXXX:8123"
export ES_USER="hass"
export ES_PASS="XXXXXX"
export ES_URL="https://XXXXXX:443"
python3 app.py
