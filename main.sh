#!/bin/bash
# This is a simple shell script

cd scraping
python ryanair.py
python transaviaApi.py
python tui.py

if [ "$1" == "BRU" ]; then
  python brusselsAirlines.py
fi
