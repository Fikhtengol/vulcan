#! /usr/bin/env python
from random import shuffle
import os
import sys
def myshuffle(infile):
	"""just shuffle small than 100w lines'file. once more than ,drop."""
	xs=[]
	for line in open(infile):
		xs.append(line.strip())
		if len(xs) == 1000000:
			shuffle(xs)
			for x in xs:
				print x
			xs=[]
	shuffle(xs)
	for x in xs:
		print x

if __name__=="__main__":
	myshuffle(sys.argv[1])
