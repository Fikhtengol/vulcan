try:
    import codecs
except ImportError:
    codecs = None
import time, os
import logging
import logging.handlers

def get_timedrotating_logger(log_filename='log.log', naming='MyLogger', level=logging.DEBUG, when='d', interval=1, backupCount=365):
    # Set up a specific logger with our desired output level                                                                                      
    logger = logging.getLogger(naming)
    logger.setLevel(level)

    # Add the log message handler to the logger                                                                                                   
    formatter = logging.Formatter('%(asctime)s - %(filename)s:%(funcName)s:%(lineno)d - %(name)s - %(levelname)s - %(message)s')
    handler = logging.handlers.TimedRotatingFileHandler(log_filename, when=when, interval=interval, backupCount=backupCount,)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

class MZTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
  def __init__(self, dir_log, category, machineid, zone, project, module, when='d', interval=1):
   self.dir_log = dir_log
   self.category = category
   self.machineid = machineid
   self.zone = zone
   self.project = project
   self.module = module
   self.when = when
   self.interval = interval
   self.timeformat = '%Y%m%d%H%M%S'
   if self.when == 's':
       self.timeformat = '%Y%m%d%H%M%S'
   elif self.when == 'm':
       self.timeformat = '%Y%m%d%H%M'
   elif self.when == 'h':
       self.timeformat = '%Y%m%d%H'
   elif self.when == 'd':
       self.timeformat = '%Y%m%d'
   filename =  os.path.join(self.dir_log, '%s-%s-%s-%s-%s-%s.log' %(time.strftime(self.timeformat), self.category, self.machineid, self.zone, self.project, self.module))
   logging.handlers.TimedRotatingFileHandler.__init__(self,filename, when=self.when, interval=self.interval, backupCount=0, encoding=None)

  def doRollover(self):
   """
   TimedRotatingFileHandler remix - rotates logs on daily basis, and filename of current logfile is time.strftime("%m%d%Y")+".txt" always
   """ 
   self.stream.close()
   # get the time that this sequence started at and make it a TimeTuple
   t = self.rolloverAt - self.interval
   timeTuple = time.localtime(t)
   self.baseFilename = os.path.join(self.dir_log, '%s-%s-%s-%s-%s-%s.log' %(time.strftime(self.timeformat), self.category, self.machineid, self.zone, self.project, self.module))
   if self.encoding:
     self.stream = codecs.open(self.baseFilename, 'w', self.encoding)
   else:
     self.stream = open(self.baseFilename, 'w')
   self.rolloverAt = self.rolloverAt + self.interval

def get_mztimedrotating_logger(log_dir, category, machineid, zone, project, module, naming='MyLogger', level=logging.DEBUG, when='d', interval=1):
    # Set up a specific logger with our desired output level                                                                                      
    logger = logging.getLogger(naming)
    logger.setLevel(level)

    # Add the log message handler to the logger                                                                                                   
    formatter = logging.Formatter('%(levelname)s [%(asctime)s] [%(created)f] [%(threadName)s] [%(name)s:%(funcName)s()] (%(filename)s:%(lineno)d) %(message)s')
    handler = MZTimedRotatingFileHandler(log_dir, category, machineid, zone, project, module, when, interval)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

if __name__ == '__main__':
    category = 'debug'
    machineid = '27'
    zone = 'cn'
    project = 'guard100'
    module = 'supervision77'

    logger = log4py.get_mztimedrotating_logger('.', category, machineid, zone, project, module, 'Supervision', when='m')
    logger.info('good')
    time.sleep(65)

    logger.info('better')
    time.sleep(65)
    
    time.sleep(65)
    logger.info('best')
