#!/bin/bash
# This is a simple shell script


python3 scraping/ryanair.py
python3 scraping/transaviaApi.py
python3 scraping/tui.py

if [ "$1" == "BRU" ]; then
  python brusselsAirlines.py
fi
