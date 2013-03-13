#! /usr/bin/env python
import os
import sys
import threading
import time
import sventypes
import  shutil

class Outer(threading.Thread):
	"""each inval  output queue.output to destdir,named by time """
	def __init__(self,queue):
		threading.Thread.__init__(self) 
		self.queue=queue
	def run(self):
		print 'outer starting...'
		inval=10*60
		lasttime=nowtime=time.time()
		while self.queue.nomore != 2:
			sleeptime=time.time()-lasttime
			if sleeptime < inval:
				time.sleep(inval - sleeptime)
				continue
			lasttime = time.time()
			fname = time.strftime("%Y%m%d%H%M%S.dat", time.localtime())
			fcont = self.queue.doout()
			if len(fcont.strip()) == 0:
				continue
			fp=open(sventypes.Task.destdir+"/."+fname,"wb")
			fp.write(fcont)
			fp.flush()
			fp.close()
			shutil.move(sventypes.Task.destdir+"/."+fname,sventypes.Task.destdir+"/"+fname)
		if self.queue.output != "":
			fname = time.strftime("%Y%m%d%H%M%S.dat", time.localtime())
			fcont = self.queue.doout()
			fp=open(sventypes.Task.destdir+"/"+fname,"wb")
			fp.write(fcont)
			fp.flush()
			fp.close()
