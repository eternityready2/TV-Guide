#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $DIR
echo "Doing"
nohup venv/bin/python3.8 site/server.py 2>&1 > /dev/null &


#disown
#disown
echo $! >./running.pid
echo "Done"
