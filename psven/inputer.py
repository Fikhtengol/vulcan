#! /usr/bin/env python
import os
import sys
import threading
import time
import  shutil
import ConfigParser
import string, os, sys
import sventypes
def load_config():
	if not os.path.exists("psven.conf"):
		return
	try:
		cf = ConfigParser.ConfigParser()
		cf.read("psven.conf")
		sventypes.Politeness.Inval = cf.getint("psven","PoliteInval")
		#print sventypes.Politeness.Inval
	except Exception,e:
		print e
def synchronized(method):
	""" Work with instance method only !!! """
	def new_method(self, *arg, **kws):
		with self.lock:
			return method(self, *arg, **kws)
	return new_method
class Inputer(threading.Thread ):
	""" each 5s search file in homedir,add to flages and files"""
	lock = threading.RLock()
	def __init__(self,homedir):
		threading.Thread.__init__(self)
		self.setDaemon(1)# once main thread stoped,child thread be killed like c/c++ . in python,defalutly,main thread will wait until  child thread over
		self.homedir=homedir
		self.running = 1
		self.files =  []
		self.flags = {}# {file:ctime}
		self.passtime = 10
		if not os.path.exists(homedir):
			raise exception,'bad homedir'
	@synchronized
	def add_task(self,s):
		if s not in self.files:
			self.files.append(s)
	@synchronized
	def get_task(self):
		if len(self.files)==0:
			return None
		return os.path.join(self.homedir,self.files.pop(0))

	def run(self):
		print 'inputer starting...'
		while self.running:
			ss=os.listdir(self.homedir)
			for s in ss:
				if not s.endswith('.urllist'):
					continue
				ctime=0
				try:
					fstat=os.stat(os.path.join(self.homedir,s))
					ctime=fstat.st_ctime
				except:
					continue
				if self.flags.has_key(s):#s exist,and the ctime newer than passtime,update ctime to flag
					if  ctime - self.flags[s] > self.passtime:
						self.add_task(s)
						self.flags[s]=ctime
				else:#s is new file . just add
					self.flags[s]=ctime
					self.add_task(s)
			time.sleep(5)
			load_config()

if __name__=="__main__":
	inputer = Inputer("input")
	inputer.start()
	inputer.join()
