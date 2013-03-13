#! /bin/sh
cd /home/data/psven
sh stop.sh -9
nohup ./run.sh svenin svenout >& nohup.out &
