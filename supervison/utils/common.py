#!/bin/env python
import subprocess

import os, os.path, re
import shutil
import time
class Common():
    """
    Class: Common
    Description: Aggregate several common function here
    """
    
    def isEmptyStr(inStr):
        """
        Summary: determine whether a string is empty or not
        Parameter:
            inStr -- the string need to be determined
        Return
            return True if the inStr is empty, otherwise return False
        """
        if not inStr or len(inStr.strip()) == 0:
            return True
        else:
            return False
    isEmptyStr = staticmethod(isEmptyStr)

    def validNotEmptyStr(inStr, name):
        """
        Summary:  ensure the inStr is not an empty string
        Parameter:
            inStr -- the string need to be determined
            name  -- the name of the inStr
        Return
            If the inStr is empty, raise an exception
        """        
        if Common.isEmptyStr(inStr) == True:
            raise Exception("%s couldn't has empty value" % (str(name), ))
    validNotEmptyStr = staticmethod(validNotEmptyStr)

    def isExistingFile(fileName):
        """
        Summary: determine whether a file is existing or not
        Parameter:
            fileName -- the file need to be determined
        Return
            return True if the file exists, otherwise return False        
        """
        if Common.isEmptyStr(fileName):
            return False
        if not os.path.exists(fileName):
            return False
        else:
            return True
    isExistingFile = staticmethod(isExistingFile)

    def validExistingFile(fileName, name):
        """
        Summary: ensure file is existing
        Parameter:
            fileName -- the file need to be determined
            name     -- the name of the fileName
        Return
            raise exception if the file doesn't exist.
        """        
        if Common.isExistingFile(fileName) == False:
            raise Exception("File [%s] with path [%s] doesn't exist" % (str(name), str(fileName)))
    validExistingFile = staticmethod(validExistingFile)

    def isNone(obj):
        """
        Summary: determine whether an object is None or not
        Parameter:
            obj -- the object need to be determined
        Return
            return True if the object is None, otherwise return False        
        """        
        if not obj:
            return True
        else:
            return False
    isNone = staticmethod(isNone)

    def validNotNone(obj, name):
        """
        Summary: ensure an object is not None
        Parameter:
            obj  -- the object need to be determined
            name -- name of the obj
        Return
            raise exception if the obj is None
        """                
        if Common.isNone(obj):
            raise Exception("%s couldn't be None" % (str(name),))
    validNotNone = staticmethod(validNotNone)

    def removePath(path):
        """
        Summary:    remove a directory or a file
        Parameter:
            path -- the path of the dir or the file
        Return
            No return value
        """                        
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                #os.removedirs(path)
                shutil.rmtree(path, True)
    removePath = staticmethod(removePath)

    def basename(path):
        while True:
            if path.endswith('/'):
                path = path[0:len(path)-1]
            else:
                break
        return os.path.basename(path)
    basename = staticmethod(basename)

    def is_valid_hostname(hostname):
        if len(hostname) > 255:
            return False
        if hostname[-1:] == ".":
            hostname = hostname[:-1] # strip exactly one dot from the right, if present
        allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in hostname.split("."))
    is_valid_hostname = staticmethod(is_valid_hostname)

    def addPATH():
        pwd = os.getcwd()
        cmd = sys.argv[0]
        path = os.path.dirname(os.path.join(pwd, cmd))
        sys.path.append(os.path.join(path, '..'))
    addpath = staticmethod(addPATH)

    def cmd(cmd):
        res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True);
        ret = res.stdout.readlines()
        return ret
    cmd = staticmethod(cmd)



    def protect_run(method):
        """make sure method work"""
        def new_method(self,*arg,**kws):
            work_pid=os.fork()
            if not work_pid:
                #child 
                method(self,*arg,**kws)
                #child process exit, restarting                
            done=os.wait()
            time.sleep(1)
            method(self,*arg,**kws)
        return new_method
    protect_run = staticmethod(protect_run)

if __name__ == "__main__":
    print Common.basename('/home/supertool/guard/carrier')
    print Common.basename('/home/supertool/guard/carrier/')
    print Common.basename('/home/supertool/guard/carrier/////')
