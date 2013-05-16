#! /usr/bin/evn python
import threading
import time
import sventypes
import sys
import os, sys
import logging
from log import LOG
#try:
#	from cStringIO import StringIO
#except ImportError:
#	from StringIO import StringIO
import pycurl

class worker(threading.Thread):  
	lock = threading.RLock()
	agents=["Mozilla/5.0 (compatible; heritrix/1.10.2 +http://i.stanford.edu/)","Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)","Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)","Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)","Mozilla/4.0 (compatible; MSIE 5.0; Windows NT)","Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13"]
	def __init__(self,no,q,num_conn,proxy):   
		threading.Thread.__init__(self)        
		self.setDaemon(1)
		self.no=no 
		self.queue=q
		self.proxy=proxy
		# Pre-allocate a list of curl objects
		self.m = pycurl.CurlMulti()
		self.m.handles = []
		for i in range(num_conn):
			c = self.init_conn()
			self.m.handles.append(c)
	def init_conn(self):
		c = pycurl.Curl()
		c.setopt(pycurl.FOLLOWLOCATION, 1)
		c.setopt(pycurl.MAXREDIRS, 5)
		c.setopt(pycurl.CONNECTTIMEOUT, 5)
		c.setopt(pycurl.DNS_USE_GLOBAL_CACHE,1)
		c.setopt(pycurl.DNS_CACHE_TIMEOUT,3600*24)
		c.setopt(pycurl.USERAGENT,"Mozilla/5.0 (compatible; heritrix/1.10.2 +http://i.stanford.edu/)")
		c.setopt(pycurl.ENCODING,"gzip")
		c.setopt(pycurl.TIMEOUT, 15)
		c.setopt(pycurl.NOSIGNAL, 1)
		c.usedtimes=0
		pxy = self.proxy.get()
		c.pxy=""
		if pxy!=None:
			c.pxy=pxy
			c.setopt(pycurl.PROXY,pxy)
			c.setopt(pycurl.HTTPPROXYTUNNEL,1)
		return c
	def run(self): 
	  # Main loop
	  print 'worker',self.no,'starting...'
	  SIGN = "MZLIUPEIZHARUIMM:"
	  freelist = self.m.handles[:]
	  num_processed = 0 
	  num_tasks = 0
	  while self.queue.on() or num_tasks > num_processed:
	  #while self.queue.size()>0  or num_tasks > num_processed:
		# If there is an url to process and a free curl object, add to multi stack
		while self.queue.size()>0 and freelist:
			c=freelist.pop()
			if c.usedtimes > 30:
				c.close()
				c=self.init_conn()
			task = self.queue.pop(c.pxy)
			if task==None:
				freelist.append(c)
#				time.sleep(1)
				break
			task.clear()
			task.firstline=SIGN+task.url
			c.setopt(pycurl.URL, task.url)
			c.setopt(pycurl.WRITEFUNCTION,task.do)
			self.m.add_handle(c)
			# store some info
			c.task = task
			c.usedtimes += 1
			c.start_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
			num_tasks += 1
		# Run the internal curl state machine for the multi stack
		while 1:
			ret, num_handles = self.m.perform()
			if ret != pycurl.E_CALL_MULTI_PERFORM:
				break
		# Check for curl objects which have terminated, and add them to the freelist
		with self.lock:
		  nowtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
		  while 1:
			num_q, ok_list, err_list = self.m.info_read()
			for c in ok_list:
				hcode = c.getinfo(pycurl.HTTP_CODE)
				if hcode >= 200 and hcode < 400:
					LOG.info("Success: "+c.start_time+"\t"+nowtime+"\t"+str(c.task.id)+"\t"+"httpcode="+str(c.getinfo(pycurl.HTTP_CODE))+"\t"+c.task.url)
					htmllen=len(c.task.html)+1
					c.task.firstline +="\t"+c.getinfo(pycurl.EFFECTIVE_URL)+"\t"+str(htmllen)
					self.queue.saveme(c.task.firstline+"\n"+c.task.html+"\n")
				else:
					LOG.info("BadResponse: "+c.start_time+"\t"+nowtime+"\t"+str(c.task.id)+"\t"+"httpcode="+str(c.getinfo(pycurl.HTTP_CODE))+"\t"+c.task.url)
				self.m.remove_handle(c)
				freelist.append(c)
			for c, errno, errmsg in err_list:
				c.task.retry += 1
				if c.task.can_try():
					self.queue.push(c.task)
				if c.task.can_try():
					LOG.info("Retry: "+c.start_time+"\t"+nowtime+"\t"+str(c.task.id)+"\t"+str(c.task.retry)+"\t"+c.task.url+"\t"+str(errno)+"\t"+errmsg)
				else:
					LOG.info("Failed: "+c.start_time+"\t"+nowtime+"\t"+str(c.task.id)+"\t"+str(c.task.retry)+"\t"+c.task.url+"\t"+str(errno)+"\t"+errmsg)
				self.m.remove_handle(c)
				c.close()
				c=self.init_conn()
				freelist.append(c)
			num_processed = num_processed + len(ok_list) + len(err_list)
			if num_q == 0:
				break
			# Currently no more I/O is pending, could do something in the meantime
			# (display a progress bar, etc.).
			# We just call select() to sleep until some more data is available.
		self.m.select(1.0)
	  # Cleanup
	  for c in self.m.handles:
			c.close()
	  self.m.close()
	  #print 'thread ',self.no,' exited'
