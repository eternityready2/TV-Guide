#!/bin/bash
cd /home/manager/chg
source venv/bin/activate
python3.8 site/server.py 2>&1 > /dev/null 
