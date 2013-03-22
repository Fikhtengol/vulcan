#! /usr/bin/env python
import logging
from logging.handlers import TimedRotatingFileHandler
def init_log():
	LOG=logging.getLogger('psven')
	LOG.setLevel(logging.INFO)
	#console = logging.StreamHandler()
	filer = TimedRotatingFileHandler('log/psven.log','midnight')
	filer.suffix = "%Y-%m-%d"
	#LOG.addHandler(console)
	LOG.addHandler(filer)
	return LOG
LOG=init_log()
