#! /usr/bin/env python
import os
import sys
def parse(infile):
	mm = {}
	ifile = open(infile,"rb")
	count = 0
	while ifile:
		count += 1 
		line = ifile.readline()
		if line.strip() == "":
			return mm
		if line.find("MZLIUPEIZHARUIMM:")!=0:
			print "big error:",line
		i=line.find("\t")
		url=line[len("MZLIUPEIZHARUIMM:"):i]
		length=int(line[i+1:].strip())
		cont=ifile.read(length)
		mm[url]=cont

if __name__ == "__main__":
	parse(sys.argv[1])
