import os
import config
import sys
from utils.filedb import Filedb

if __name__=="__main__":
    fdb=Filedb(config.db_file)
    if len(sys.argv)!=3:
        print "Usage: %s opt:[add,remove] ip " % sys.argv[0]
        sys.exit(1)
    worker=sys.argv[2]
    #yes=checkip(worker)
    yes=True
    if not yes:
        print "not valid ip:%s"%(worker)
        sys.exit(1)
    workers=fdb.get()
    if workers==None:
        workers=[]
    has_worker=False
    if worker in workers:
        has_worker=True
    if sys.argv[1]=="add":
        if has_worker:
            print "worker:%s has been added"%(worker)
            sys.exit(1)
        sys.argv[1]
        workers.append(worker)
        fdb.save(workers)
    elif sys.argv[1]=="remove":
        if not has_worker:
            print "worker:%s has not been  added"%(worker)
            sys.exit(1)
        workers.remove(worker)    
        fdb.save(workers)
    else:
            print "Usage: %s opt:[add,remove] ip " % sys.argv[0]
            sys.exit(1)
    print fdb.get()
