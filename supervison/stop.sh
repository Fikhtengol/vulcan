#! /bin/sh
PROCESSID=$(ps aux | grep python| grep scheduler | grep -v \"ssh\|bash\|grep\" | awk '{print $2}')
kill $1 $PROCESSID
