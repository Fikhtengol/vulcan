#encoding=utf-8
import commands
import config
import redis
import time
import os

class Monitor():
    def __init__(self,):
        self.rs=redis.StrictRedis(host=config.supervison, port=config.redis_port,db=0)
        self.send_time=2
        self.listlen=(lambda time:time*60/self.send_time)(120)
    def top(self,):
        cmd = '''export LANG=C ; top -n 1 -b'''
        (status,output) = commands.getstatusoutput(cmd)
        if status!=0:
            #return False,"failed on run top to get machine info:%s"%(status)
            return None
        return output.split('\n')
    def sar(self,):
        cmd = '''export LANG=C ; sar -n DEV 1 1'''
        status,output = commands.getstatusoutput(cmd)
        if status!=0:return None
        return output.split('\n')
        
    def machine_check(self,):
        top_output=self.top()
        if top_output==None :return 
        #cpu_info
        cpu_info=100-float(top_output[2].split(',')[3].split()[0].replace('%id',''))
        cpu_info="%.2f"%(cpu_info)
        #mem_info
        mem_info=top_output[3].split(',')
        mem_info=float(mem_info[1].split()[0].replace('k',''))/int((mem_info[0]).split()[-2].replace('k',''))*100
        mem_info="%.2f"%(mem_info)
        #net_info
        sar=self.sar()
        rx=0.0
        tx=0.0

        if sar==None:return 
        for item in sar[3:-1]:
            if item=="":break
            rx=float(item.split()[4])+rx
            tx=float(item.split()[5])+tx
        rx,tx="%.2f"%(rx),"%.2f"%(tx)
        return [cpu_info,mem_info,[rx,tx]]
    
    def send_to_redis(self,):
        name=config.localhost+"_minfo"
        while True:
            machine_info=self.machine_check()
            print machine_info
            if machine_info==None: return
            if self.rs.llen(name)>=self.listlen:
                self.rs.rpop(name)
            self.rs.lpush(name,machine_info)
            time.sleep(self.send_time)

    def run(self,):
        work_pid = os.fork()
        if not work_pid:
            m.send_to_redis()
            # child process exit, restarting
        done = os.wait()
        time.sleep(1)
        self.run()
        

if __name__=="__main__":
    m=Monitor()
    m.send_to_redis()
