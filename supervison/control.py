import config
import commands
class control():
    def __init__(self,machine):
        self.psven_path = config.psven_path
        self.remote_machineip = machine.items()[0][1]
        self.remote_path = config.remote_path
        self.remote_user = config.remote_user

        
    def deploy(self,):

        deploy_cmd = '''ssh -o StrictHostKeyChecking=no %s@%s "mkdir -p %s" ; rsync -avz %s/ %s@%s:%s''' %(self.remote_user, self.remote_machineip, self.remote_path, self.psven_path, self.remote_user, self.remote_machineip, self.remote_path)
        try:
            (status,output) = commands.getstatusoutput(deploy_cmd)
            if status != 0:
                return (False, output)
        except Exception,e:
            print e
            return False,e

        return True,""
        
    def start(self):
        run_cmd = '''ssh -o StrictHostKeyChecking=no %s@%s  "cd %s; python psven.py svenout > /dev/null 2>&1 &"''' %(self.remote_user, self.remote_machineip,self.remote_path)
        print run_cmd
        (status,output) = commands.getstatusoutput(run_cmd)
        if status != 0:
            return (False, output)
        
        return True,""

if __name__ == "__main__": 

    c=control({"trek1":"127.0.0.1"})

    c.start()
    
