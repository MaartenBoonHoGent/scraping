#!/bin/bash
# This is a simple shell script


python3 scraping/ryanair.py
wait
python3 scraping/transaviaApi.py
wait
python3 scraping/tui.py
wait
if [ "$1" == "BRU" ]; then
  python brusselsAirlines.py
fi
