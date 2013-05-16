#encoding=utf-8
import time
import redis
import os
import ConfigParser
config = ConfigParser.ConfigParser()
config.read('my.conf')
redis_host=config.get('redis','redis_host')
redis_port=config.get('redis','redis_port')
redis_port=int(redis_port)
class Listen():
    """listen info from psven
    """
    @staticmethod
    def get_lastest_info(ip):
        
        '''return the  machine's info from redis '''
        rs=redis.StrictRedis(host=redis_host, port=redis_port,db=0)
        name=ip+"_minfo"
        if rs.llen(name)!=0:
            info=rs.lindex(name,0)
            return info
        return None
    @staticmethod
    def get_all_info(ip):
        """get init meminfo from redis"""
        res=[]

        rs=redis.StrictRedis(host=redis_host, port=redis_port,db=0)
        name=ip+"_minfo" 
        print  rs.llen(name)
        for it in range(rs.llen(name),0,-1):
            item=rs.lindex(name,it)
            if item:
                res.append(item)
        return res
if __name__=="__main__":
    #print Listen.listen("127.0.0.1")
    for it in Listen.get_all_info('127.0.0.1'):
        print it

