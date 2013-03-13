#! /bin/sh
export LD_LIBRARY_PATH=./lib/:$LD_LIBRRARY_PATH
export PYTHONPATH=./site-packages:$PYTHONPATH:/usr/lib/
export PYTHONEXE=/usr/bin/python2.7
sh conti.sh
#/usr/local/bin/python2.6 shuffle.py $1 > shuffle_res.urls
#/usr/local/bin/python2.6 psven.py shuffle_res.urls $2 $3 $4
$PYTHONEXE psven.py $1 $2 $3 $4  

