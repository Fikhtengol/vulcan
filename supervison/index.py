
import os
import web
from view import render
import pickle as p
import control
import listen


from ClusterManagement.web  import  controller

urls=(
    '/','index',
    '/machinelist','machinelist',
    '/checkmachine','checkmachine',
    '/deploynew','deploynew',
    '/machine_list','machine_list',
    '/start','start',
    '/machine_info','machine_info',
    '/init_info','init_info',
    '/get_info','get_info',
    '/ClusterManagment',controller.clusterapp,

)
class index:
    def GET(self,):
        return render.index()



        
class machine_list:
    def GET(self,):
        return render.machine_list()
class checkmachine:
    
    def GET(self,):
        mdict={}        
        new=eval(web.input()["machine"])
        new_host=new.keys()[0]
        new_ip=new[new_host]
        try :
            with open('.mfile',"rb") as f:
                mdict=p.load(f)
        except Exception,e:
            #TODO:1.put into log.2.open failed
            print e
            open('.mfile',"wb")
            return [new,""]
        
        if new_host  in mdict.keys():
            return ["0","host has been used"]
        if new_ip in mdict.values():
            return ["1","machine with the ip:%s has been deployed"%(new_ip)]
        return [new,""]

class deploynew:
    def GET(self,):
        mdict={}        
        new=eval(web.input()["machine"])
        c=control.control(new)
        res,msg=c.deploy()
        res=True
        if res:
            try:
                f=open ('.mfile','rb')
                try:
                    mdict=p.load(f)
                except EOFError:
                    mdict={}
                    pass
                mdict.update(new)
                with open('.mfile','wb') as f:
                    p.dump(mdict,f)
            except Exception,e:
                return e
        return msg

class start:
    def GET(self,):
        i=eval(web.input()["machine"])
        c=control.control(i)
        #res,msg=c.start()
        res=True
        if res:
            return "success";
        else:
            return msg
        
        
            

        
class machine_list:
    def GET(self,):
        mdict={}
        try :
            with open('.mfile',"rb") as f:
                mdict=p.load(f)
        except Exception,e:
            #TODO:1.put into log.2.open failed
            print e
            open('.mfile',"wb")
        
        return render.machine_list(mdict)
class machine_info:
    def GET(self,):
        ip=web.input()['ip']
        
        return render.machine_info(ip)
class get_info:
    def GET(self,):
        ip=web.input()['ip']
        info=listen.Listen.listen(ip)
        if info==None:
            return None
        info=list(eval(info))
        info[2]=list(info[2])
        return info
class init_info:
    def GET(self,):
        ip=web.input()['ip']
        info=listen.Listen.listenall(ip)
        if info==None:return None
        return info
if __name__ == "__main__": 
    app = web.application(urls, globals())
    app.run()
