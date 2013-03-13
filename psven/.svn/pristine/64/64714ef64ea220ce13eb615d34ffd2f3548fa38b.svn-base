#! /usr/local/bin/python2.6
import os
import sys
import parse_cont
import md5
import difflib
key = md5.new()
comres={}
comcnt={}
class CmpObj:
	def __init__(self):
		self.urls=[]
		self.match=difflib.SequenceMatcher()
		self.ratios=[]
	def add(self,url,content):
		if len(self.urls) == 0:
			self.urls.append(url)
			self.match.set_seq2(content)
			self.ratios.append(0)
		else:
			self.urls.append(url)
			self.match.set_seq1(content)
			self.ratios.append(self.match.quick_ratio())
			self.match.set_seq2(content)
	def __str__(self):
		outstr=str(len(self.urls))+"\t"
		for u in self.urls:
			outstr+=u+"\t"
		outstr+='\n'
		outstr+=str(len(self.ratios))+"\t"
		for r in self.ratios:
			outstr+=str(r)+"\t"
		return outstr

def do_print(comres):
	for m in comres.values():
		if len(m.urls) <= 1:
			continue
		print str(m)

for f in os.listdir(sys.argv[1]):
	print f
	mm=parse_cont.parse(os.path.join(sys.argv[1],f))
	for m in mm.keys():
		idx =m.find("?")
#		url = m
		if idx != -1:
			url = m[0:idx]
		else:
			continue
		if comres.has_key(url):
			comres[url].add(m,mm[m])
		else:
			com=CmpObj()
			com.add(m,mm[m])
			comres[url]=com
#		if len(comres.keys()) % 1000 ==0:
#			do_print(comres)
do_print(comres)


"""				
def do_print(comres,comcnt):
  for m in comres.keys():
	if len(comres[m]) == comcnt[m]:
		continue
	outstr=m+"\t"+str(len(comres[m]))+"\t"+str((comcnt[m]))
	for v in comres[m]:
		outstr+="\t"+str(v)
	print outstr
	
for f in os.listdir(sys.argv[1]):
	mm=parse_cont.parse(os.path.join(sys.argv[1],f))
	for m in mm.keys():
		idx =m.find("?")
#		url = m
		if idx != -1:
			url = m[0:idx]
		else:
			continue
		h=hash(mm[m])
	#key.update(mm[m])
		if comres.has_key(url):
			comcnt[url]+=1
			#comres[url].add(key.hexdigest())
			comres[url].add(h)
		else:
			comcnt[url]=1
			comres[url]=set()
			#comres[url].add(key.hexdigest())
			comres[url].add(h)
#		if len(comres.keys()) % 10000 == 0 :
			print len(comres.keys())
			do_print(comres,comcnt)



do_print(comres,comcnt)
"""
