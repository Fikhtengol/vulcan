#! /usr/bin/env python
import os 
import sys
for line in open(sys.argv[1]):
	i=line.find("\t")
	if i==-1:
		continue
	line = line[0:i]
	print line
