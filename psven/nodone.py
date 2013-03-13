#! /usr/bin/env python
import os
import sys
from random import shuffle
#output the urls which unsucessful in log.
ins={}# search the homedir for urls,add to ins. url:0
fins={}# search log of unsucessful urls,add to fins,url:0
for f in os.listdir(sys.argv[1]):
	if not f.endswith(".urllist"):
		continue
	for line in open(os.path.join(sys.argv[1],f)):
		ins[line.strip()]=0
for f in os.listdir(sys.argv[2]):
	if f.find(".log") == -1:
		continue
	for line in open(os.path.join(sys.argv[2],f)):
		if line.find("Success")!=-1:
			ss=line.strip().split("\t")
			fins[ss[len(ss)-1]]=0
# delete the url in ins,which alse in fins.
for key in fins.keys():
	if ins.has_key(key):
		del ins[key]

keys = ins.keys()
shuffle(keys)
for key in keys:
	print key


