import config
import redis
import inputer
import time
import os
from hash_ring import HashRing
class Scheduler():
    def __init__(self,):
        '''
        init redis with the config. start a inter thread. 
        and  hashring with replication.
        '''
        self.rs=redis.StrictRedis(host=config.redis_host, port=config.redis_port,db=0)
        self.inter=inputer.Inputer(config.input_home)
        self.inter.start()
        #TODO:add the weight for hashring() init
        self.hashring=HashRing(nodes=config.workers,replicas=100
)
        self.nodes={}
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
    s=Scheduler()
    s.run()
