import config
import commands
import scheduler
import sys
class control():
    def __init__(self,config):
        self.psven_path = config.psven_path
        #machine = machine.items()[0][1]
        self.remote_path = config.remote_path
        self.remote_user = config.remote_user

    def run_cmd(self,cmd):
        try:
            (status,output) = commands.getstatusoutput(cmd)
            if status != 0:
                return (False, output)
        except Exception,e:
            print e
            return False,e
        return True,""

    def deploy(self,machines):
        res=[]
        for machine in machines:
            deploy_cmd = '''ssh -o StrictHostKeyChecking=no %s@%s "mkdir -p %s" ; rsync -avz %s/ %s@%s:%s''' %(self.remote_user, machine, self.remote_path, self.psven_path, self.remote_user, machine,self.remote_path)
            print deploy_cmd
            res.append(self.run_cmd(deploy_cmd))

        return res
    
    def start(self,machines):
        res=[]
        for machine in machines:
            start_cmd = '''ssh -o StrictHostKeyChecking=no %s@%s  "cd %s; python psven.py svenout > /dev/null 2>&1 &"''' %(self.remote_user, machine,self.remote_path)
            print start_cmd
            res.append(self.run_cmd(start_cmd))
        return res

    def stop(self,machines):
        res=[]
        for machine in machines:

            stop_cmd = '''ssh -o StrictHostKeyChecking=no %s@%s  "cd %s; /usr/bin/env bash stop.sh > /dev/null 2>&1 &"''' %(self.remote_user, machine,self.remote_path)
            res.append(self.run_cmd(stop_cmd))
            print stop_cmd
        return res
        
if __name__ == "__main__": 
    c=control(config)
    machine=[]
    if len(sys.argv)!=3:
        print "Usage: %s opt:[deploy,start,stop] machine_list " % sys.argv[0]
        sys.exit(1)
    
    try:
        opt=eval("c."+sys.argv[1])
        machine.append(sys.argv[2])
        opt(machine)
    except Exception,e:
        print e
	print "Usage: %s opt:[deploy,start,stop] machine_list " % sys.argv[0]
	raise SystemExit

