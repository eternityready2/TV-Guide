#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $DIR
# /usr/local/bin/python3.8 site/do_scrape.py

source /home/manager/chg/venv/bin/activate
python /home/manager/chg/site/do_scrape.py
curl http://localhost/live-tv/update
#curl http://server.home/update
