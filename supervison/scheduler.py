import config
import redis
import time
import os
from hash_ring import HashRing
from utils.filedb import Filedb
import inputer
class Scheduler():
    def __init__(self,):
        '''
        init redis with the config. start a inter thread.
        hashring with replication
        inworker is a thread can push or get worker from it.
        '''
        self.rs=redis.StrictRedis(host=config.redis_host, port=config.redis_port,db=0)
        self.inter=inputer.Inputer(config.input_home)
        self.db=Filedb(config.db_file)
        self.workers=self.db.get()
        self.time=time.time()
        #TODO:add the weight for hashring() init

        self.hashring=HashRing(nodes=self.workers,replicas=100)
        self.nodes={}
    
    def reload_worker(self,):
        ctime=time.time()
        if ctime-self.time>1:
            new_workers=self.db.get()
            if new_workers!=self.workers:
                news=[var for var in new_workers if var not in self.workers]
                for new in news:
                    self.hashring.add_node(new)
                deles=[var for var in self.workers if var not in new_workers]
                for dele in deles:
                    self.hashring.remove_node(dele)
                self.workers=new_workers
            self.time=ctime
        
        
    def pushurl(self,url):
        #TODO:rs push failed!
        node=self.hashring.get_node(url)
        self.rs.lpush(node,url)
        if node not in self.nodes.keys():
            self.nodes[node]=0
        self.nodes[node]+=1
        return node

    def get_nodes(self,):
        for node in self.nodes.keys():
            print node+":"+str(self.nodes[node])

    def run(self,):
        self.inter.start()
        while self.inter.running:
            ifile = self.inter.get_task()
            if ifile == None:
		time.sleep(3)
		continue
            if not os.path.exists(ifile):
		time.sleep(3)
		continue

            try:
		for line in open(ifile):
                    if line.strip()!="":
                        node=self.pushurl(line.strip())
                    while self.rs.llen(node)>=1000000:
                        time.sleep(1)
                    if self.inter.running == 0:
                        break
                    self.reload_worker()
                self.get_nodes()
            except Exception,e:
                #TODO:write to log
                print str(e)
		continue

if __name__=="__main__":
    sl=Scheduler()
    sl.run()
