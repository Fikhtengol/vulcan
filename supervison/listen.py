#encoding=utf-8
from utils.common import Common
import config
import time
import redis
import os
class Listen():
    """listen info from psven
    """
    @staticmethod
    def listen(ip):
        
        '''return the  machine's info from redis '''
        rs=redis.StrictRedis(host=ip, port=config.redis_port,db=0)
        name=ip+"_minfo"
        if rs.llen(name)!=0:
            info=rs.lindex(name,0)
            return info
        return None
    @staticmethod
    def listenall(ip):
        """get init meminfo from redis"""
        res=[]
        rs=redis.StrictRedis(host=ip, port=config.redis_port,db=0)
        name=ip+"_minfo"        
        for it in range(rs.llen(name),0,-1):
            item=rs.lindex(name,it)
            if item:
                res.append(item)
        return res
if __name__=="__main__":
    #print Listen.listen("127.0.0.1")
    for i in  Listen.listenall("127.0.0.1"):
        print i
