class SingletonLock:
    def __init__(self, lock_path="/tmp/singleton.lock"):
        self._lock_file = lock_path
        self.fp = None
 
    def initial(self, name, lock_path):
        self._lock_file = lock_path
 
    def nb_lock(self):
        try:
            fcntl.flock(self.fp, fcntl.LOCK_EX|fcntl.LOCK_NB)
        except IOError, exc_value:
            self.fp.close()
            self.fp = None
            return False
        return True
 
    def lock(self):
        if self._fp == None:
            return False
 
        self.fp = open(self._lock_file, "w")
        fcntl.flock(self.fp, fcntl.LOCK_EX)
        return True
 
    def unlock(self):
        if self.fp == None:
            return True
        fcntl.flock(self.fp, fcntl.LOCK_UN)
        self.fp.close()
        self.fp = None
        return True
 
    def __del__(self):
        self.unlock()
