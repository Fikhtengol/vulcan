import config
import redis
import inputer
import time
import os
import pickle as p
from hash_ring import HashRing

class Scheduler():
    def __init__(self,):
        '''
        init redis with the config. start a inter thread. 
        and  hashring with replication.
        '''
        self.rs=redis.StrictRedis(host=config.redis_host, port=config.redis_port,db=0)
        self.inter=inputer.Inputer(config.input_home)
        #TODO:add the weight for hashring() init
        self.genworkers(callback=self.get_nodes4file)
        self.hashring=HashRing(nodes=self.workers,replicas=100)
        self.nodes={}
    def add_worker(self,ip):
        self.hashring.add_node(ip)
        
    def genworkers(self,callback):
        self.workers=callback()

    def get_node4db(self,):
        pass

    def get_nodes4file(self,):
        workers=[]
        try:
            f=open('.mfile','rb')
            res=p.load(f)
            workers=res.values()
        except Exception:
            workers=[]
        return workers

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
                        #is it too short?
                        time.sleep(1)

                    if self.inter.running == 0:
                        break
                self.get_nodes()
            except Exception,e:
                #TODO:write to log
                print str(e)
		continue

if __name__=="__main__":
    sl=Scheduler()
    sl.run()
