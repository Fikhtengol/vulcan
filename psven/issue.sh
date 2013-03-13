#! /bin/sh
export LD_LIBRARY_PATH=./lib/
export PYTHONPATH=./site-packages:$PYTHONPATH
export PYTHONEXE=/usr/local/bin/python2.6
#./pbloom.py
$PYTHONEXE $1 $2 $3 $4 $5 $6
