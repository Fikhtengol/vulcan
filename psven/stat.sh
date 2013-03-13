#! /bin/sh
PROCESS=$(ps aux | grep python| grep psven | grep -v \"ssh\|bash\|grep\" )
echo $PROCESS
wc -l log/*.log*

