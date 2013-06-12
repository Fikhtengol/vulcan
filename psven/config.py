import socket
try:
    localhost=socket.gethostbyname(socket.gethostname())
except Exception,e:
    print e

supervison='172.29.140.118'
redis_port=6379
