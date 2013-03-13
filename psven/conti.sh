#! /bin/sh
# output unsucessful urls to today.urllist
# mv svenin/*.urllist to svenin.old/
export LD_LIBRARY_PATH=./lib/
export PYTHONPATH=./site-packages:$PYTHONPATH
export PYTHONEXE=/usr/bin/python2.7

today=`date '+%y-%m-%d_%H%M%S'`
dest=$today.urllist
sh stop.sh -9
$PYTHONEXE nodone.py svenin/ log/ > $dest 
mv svenin/*.urllist svenin.old/
mv $dest svenin/
