#!  /usr/bin/env python

import threading
import time
import urlparse
import random

def synchronized(method):
	""" Work with instance method only !!! """
	def new_method(self, *arg, **kws):
		with self.lock:  
			return method(self, *arg, **kws)
	return new_method
class Task:
	"""a Task is a fetch object,"""
	destdir="."
	def __init__(self,id,url):
		self.id=id
		self.url=url
		self.retry=0
		self.host=""
		self.html=""
		self.firstline=""
		try:
			result=urlparse.urlparse(url)  
			self.host=result.netloc
		except Exception,e:
			pass
	def do(self, buf):
		self.html = self.html + buf
	def clear(self):
		self.html= ""
		self.firstline = ""
	def gethost(self):
		return self.host
	def can_try(self):
		return self.retry < 1

class Politeness:
	Inval = 5
	def __init__(self):
		self.hosts={} #key:time ,key=host+proxy
	def tryme(self,host,proxy=""):
		""" if key not apperd,or appeard more than Inval,return 1,else return 0"""
		key=host+" "+proxy
		if self.hosts.has_key(key):
			if time.time() - self.hosts[key] > self.Inval:
				#print 'lasttime=',self.hosts[host],'time.time=()',time.time(),
				self.hosts[key]=time.time()
				return 1
			else:
				return 0
		else:
			self.hosts[key]=time.time()
			#print 'newtime=',self.hosts[host],'time.time=()',time.time(),
			return 1
class TaskQueue:

	lock = threading.RLock()   
	def __init__(self):           
		self.polite=Politeness()
		self.count = 0
		self.queue = []#queue is a list of task
		self.nomore = 0 # 0 means keep on
		self.output = "" # urls' contents. 
	@synchronized
	def saveme(self,buf):
		self.output += buf
	@synchronized
	def clear(self):
		self.output = ""
		self.queue = []
	@synchronized
	def doout(self): #return output and clear output
		ret = self.output
		self.output = ""
		return ret
	@synchronized
	def on(self):
		return len(self.queue) > 0 or self.nomore == 0
	@synchronized
	def push(self,T):
		self.queue.append(T)
	@synchronized
	def insert(self,T):
		self.queue.insert(0,T)

	@synchronized
	def pop(self,proxy=""):
		"""pop when it's polite. """
		count = 0 #try pop time=len(queue)
		while count < len(self.queue):
			if self.nomore == 2:
				return None
			count += 1
			T=self.queue.pop(0)
			if self.polite.tryme(T.gethost(),proxy):
				return T
			else:
				self.queue.append(T)
		#if count!=0:
		#	time.sleep(1)
		return None
	@synchronized
	def size(self):
		return len(self.queue)

	@synchronized
	def inc(self):
		self.count+=1	
		return self.count

class Proxy:
	"""
	add a chan to list ,and change rate
	get a chan or None randomly by rate
	"""
	lock = threading.RLock()
	def __init__(self):
		self.rate=0
		self.channels=[]
	def add(self,chan):
		self.channels.append(chan)
		self.rate=1.0/(len(self.channels))
		if self.rate<0.1:
			self.rate*=2
	def get(self):
		if len(self.channels)==0:
			return None
		if random.random() < self.rate:
			return None
		i=random.randint(0,len(self.channels)-1)
		return self.channels[i]
