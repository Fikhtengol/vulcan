import os
import sys
from utils import log4py
log_dir = './log'
category = 'debug'
machineid = 'localhost'
zone = 'cn'
project = 'vulcan'
module = 'supervison'

if not os.path.exists(log_dir):
    try:
        os.makedirs(log_dir)
    except:
        log_dir = os.getcwd() 

logger = log4py.get_mztimedrotating_logger(log_dir, category, machineid, zone, project, module, 'MyLogger', when='d')

workers=['192.168.53.156',
         '192.168.53.157',
         '192.168.53.158',
         '127.0.0.1',
        ]
redis_host='172.29.140.118'
redis_port=6379
input_home=os.path.expanduser('~/workspaces/vulcan/supervison/loginput/')
psven_path=os.path.expanduser('~/workspaces/vulcan/psven')
remote_path=os.path.expanduser('~/public/vulcan/psven')
db_file=os.path.expanduser('~/workspaces/vulcan/supervison/filedb')
remote_user="lijun"

if not os.path.exists(psven_path):
    try:
        os.makedirs(psven_path)
    except:
        project_config_path = os.getcwd()
