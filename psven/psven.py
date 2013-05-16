#! /usr/local/bin/python2.7
import os
import sys
import time
import pycurl
import sventypes
import worker
import outer
import redis
import config
import time
# We should ignore SIGPIPE when using pycurl.NOSIGNAL - see
# the libcurl tutorial for more info.

'''
prepare inputhome,outputhome,num_conn thd_num, proxy,taskqueue,inter thread,outer thread
'''


if len(sys.argv)<2:
	print "Usage: %s [dirpath with URLs to fetch] [path of destdir] [<# of concurrent connections>] [<# of threads>] " % sys.argv[0]
	sys.exit(1)
# Get args
num_conn = 100
thd_num = 4
try:

	if len(sys.argv) >= 2:
		if os.path.exists(sys.argv[1]):
			sventypes.Task.destdir=sys.argv[1]
	if len(sys.argv) >= 3:
		num_conn = int(sys.argv[2])
	if len(sys.argv) >=4 :
		thd_num = int(sys.argv[3])
except:
	print "Usage: %s [dirpath with URLs to fetch] [path of destdir] [<# of concurrent connections>] [<# of threads>] " % sys.argv[0]
	raise SystemExit

myproxy=sventypes.Proxy()
if os.path.exists("proxy"):
	for line in open("proxy"):
		if len(line.strip())>0:
			myproxy.add(line.strip())

que=sventypes.TaskQueue()


output=outer.Outer(que)
output.start()
r=redis.StrictRedis(host=config.supervison,port=config.redis_port,db=0)
# init worker threads
ws=[]
for i in range(0,thd_num):
	w=worker.worker(i,que,num_conn,myproxy)
	ws.append(w)
	w.start()

count=0
# init taskqueue from inter,when task is more than 1000000,sleep 1

# 1.get a file from inter
# 2.if has line in file ,read line from file. init a task with the line. add task to taskqueue ;if not has line,goto 1
# 3. goto 2 
while True:
	try:
            #url=pull_url(r)
            url=r.rpop(config.localhost)
	    
	    if url is None:
		    time.sleep(3)
		    continue
	    #res=r.zadd('urldo',time.mktime(time.localtime()),url)
            count+=1
            task=sventypes.Task(count,url.strip())
            while que.size() >= 100000:
                time.sleep(1)
	    que.insert(task)
	except Exception,e:
	    print e	
            continue
for w in ws:
    w.join()
que.nomore = 2
output.join()
