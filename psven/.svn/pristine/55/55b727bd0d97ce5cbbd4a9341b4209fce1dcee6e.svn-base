#! /usr/bin/env python
import os 
import sys
from pybloom import BloomFilter
from unittest import TestSuite
if __name__=="__main__":
  ser=open("oom","rb")
  ser.seek(0)
  oom=BloomFilter.fromfile(ser)
  for f in os.listdir(sys.argv[1]):
	if f.find(".log") == -1:
		continue
	for line in open(os.path.join(sys.argv[1],f)):
		ss=line.strip().split("\t")
		if not (ss[len(ss)-1] in oom):
			print ss[len(ss)-1]


sys.exit(0)

oom = BloomFilter(capacity=1000*1000*200,error_rate=0.0001)
for f in os.listdir(sys.argv[1]):
	if f.find(".log") == -1:
		continue
	for line in open(os.path.join(sys.argv[1],f)):
		ss=line.strip().split("\t")
		oom.add(ss[len(ss)-1])
		if not (ss[len(ss)-1] in oom ):
			print ss[len(ss)-1]
ser=open("oom","wb")
oom.tofile(ser)
ser.close()
