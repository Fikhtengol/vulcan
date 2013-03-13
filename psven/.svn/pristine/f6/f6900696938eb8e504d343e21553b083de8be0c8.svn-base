#! /usr/local/bin/python2.6
import os
import sys
def start(hosts):
	startcmd="cd /home/data/psven; sh start.sh"
	for h in hosts:
	  cmd = "ssh "+h+" '"+startcmd+"'"
	  print cmd
	  os.system(cmd)
def stop(hosts):
	scmd="cd /home/data/psven; sh stop.sh"
	for h in hosts:
	  cmd = "ssh "+h+" '"+scmd+"'"
	  print cmd
	  os.system(cmd)
def forcestop(hosts):
	scmd="cd /home/data/psven; sh stop.sh -9"
	for h in hosts:
	  cmd = "ssh "+h+" '"+scmd+"'"
	  print cmd
	  os.system(cmd)

def svnup(hosts):
	scmd="cd /home/data/psven; svn up"
	for h in hosts:
	  cmd = "ssh "+h+" '"+scmd+"'"
	  print cmd
	  os.system(cmd)
def stat(hosts):
	scmd="cd /home/data/psven; sh stat.sh"
	for h in hosts:
	  cmd = "ssh "+h+" '"+scmd+"'"
	  print cmd
	  os.system(cmd)
def clearlog(hosts):
	scmd="cd /home/data/psven; rm log/*.log*"
	for h in hosts:
	  cmd = "ssh "+h+" '"+scmd+"'"
	  print cmd
	  os.system(cmd)
def execute(hosts,exe):
	scmd="cd /home/data/psven; "+exe
	for h in hosts:
	  cmd = "ssh "+h+" '"+scmd+"'"
	  print cmd
	  os.system(cmd)




if len(sys.argv)<3:
	print "Usage:",sys.argv[0],"hostlist command"
	sys.exit(0)
hosts=[]
for line in open(sys.argv[1]):
	hosts.append(line.strip())

if sys.argv[2] == 'start':
	start(hosts)
elif sys.argv[2] == 'stat':
	stat(hosts)
elif sys.argv[2] == 'stop':
	stop(hosts)
elif sys.argv[2] == 'svnup':
	svnup(hosts)
elif sys.argv[2] == 'forcestop':
	forcestop(hosts)
elif sys.argv[2] == 'clearlog':
	clearlog(hosts)
elif sys.argv[2] == 'exec':
	execute(hosts,sys.argv[3])
