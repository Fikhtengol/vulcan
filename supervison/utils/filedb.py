import cPickle as p
import os
basepath=os.path.join(os.getcwd(),"filedb")
class Filedb():
    def __init__(self,db_file=""):

        if not os.path.isfile(db_file):
            self.db_file=basepath
        else:
            self.db_file=db_file            

    def get(self,):
        try:
            pfile=None
            pfile=open(self.db_file,"rb")
            metadata=p.load(pfile)
        except Exception,e:
            print e
            metadata=None
        finally:
            if pfile:
                pfile.close()
            
        return metadata

    def save(self,data,):
        try:
            pfile=None
            pfile=open(self.db_file,'wb')
            p.dump(data,pfile)
        except Exception,e:
            print e
        finally:
            if pfile:
                pfile.close()
if __name__=="__main__":
    fdb=Filedb()
    data=[1,2,3]
    fdb.save(data)
    print fdb.get()
