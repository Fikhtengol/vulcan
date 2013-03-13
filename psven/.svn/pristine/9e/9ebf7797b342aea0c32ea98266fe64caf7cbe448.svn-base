#! /usr/local/bin/python2.6
import os
import sys
import urlparse
domains = {}
urls =  {}
dlists = []
for line in open(sys.argv[1]):
	domains[line.strip()]=0
	urls[line.strip()] = set()
	dlists.append(line.strip())
dlists.sort()
dlists.reverse()
count = 0 
for line in open(sys.argv[2]):
	try:
		result=urlparse.urlparse(line.strip())
		for key in dlists:
			if result[1].find(key)!=-1:
				domains[key] +=1
				idx = line.strip().find("?")
				if idx == -1:
					urls[key].add(line.strip())
				else:
					urls[key].add(line[0:idx])
				break
	except Exception,e:
		sys.exit(0)
	count +=1
	if count % 100000 == 0:
		outstr=""
		sum=0
		sum2=0
		for key in domains.keys():
			#outstr+=key+"="+str(domains[key])+" "+str(len(urls[key]))+"  ,  "
			outstr+=key+"\t"+str(domains[key])+"\t"+str(len(urls[key]))+"\n"
			sum+=domains[key]
			sum2+=len(urls[key])
		outstr += "sum\t"+str(sum)+"\t"+str(sum2)
		print outstr

outstr=""
sum=0
sum2=0
for key in domains.keys():
	#outstr+=key+"="+str(domains[key])+" "+str(len(urls[key]))+"  ,  "
	outstr+=key+"\t"+str(domains[key])+"\t"+str(len(urls[key]))+"\n"
	sum+=domains[key]
	sum2+=len(urls[key])
outstr += "sum\t"+str(sum)+"\t"+str(sum2)
print outstr

