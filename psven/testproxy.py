#! /usr/bin/env python
import sys, threading, Queue
import pycurl
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


# We should ignore SIGPIPE when using pycurl.NOSIGNAL - see
# the libcurl tutorial for more info.
try:
    import signal
    from signal import SIGPIPE, SIG_IGN
    signal.signal(signal.SIGPIPE, signal.SIG_IGN)
except ImportError:
    pass


# Get args
num_conn = 100
try:
    if sys.argv[1] == "-":
        proxys = sys.stdin.readlines()
    else:
        proxys = open(sys.argv[1]).readlines()
    if len(sys.argv) >= 3:
        num_conn = int(sys.argv[2])
except:
    print "Usage: %s <file of proxy> [<# of concurrent connections>]" % sys.argv[0]
    raise SystemExit

# Make a queue with (proxy, filename) tuples
queue = Queue.Queue()
for proxy in proxys:
    proxy = proxy.strip()
    if not proxy or proxy[0] == "#":
        continue
    queue.put(proxy)


# Check args
assert queue.queue, "no Proxys given"
num_proxys = len(queue.queue)
num_conn = min(num_conn, num_proxys)
assert 1 <= num_conn <= 10000, "invalid number of concurrent connections"
print "PycURL %s (compiled against 0x%x)" % (pycurl.version, pycurl.COMPILE_LIBCURL_VERSION_NUM)
print "----- Testing", num_proxys, "Proxys using", num_conn, "connections -----"


class WorkerThread(threading.Thread):
    lock=threading.RLock()   
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        while 1:
            try:
                proxy = self.queue.get_nowait()
            except Queue.Empty:
                raise SystemExit
            fp =  StringIO()
            curl = pycurl.Curl()
            curl.setopt(pycurl.URL, "http://www.tudou.com")
            curl.setopt(pycurl.FOLLOWLOCATION, 1)
            curl.setopt(pycurl.MAXREDIRS, 5)
            curl.setopt(pycurl.CONNECTTIMEOUT, 5)
            curl.setopt(pycurl.TIMEOUT, 15)
            curl.setopt(pycurl.NOSIGNAL, 1)
            curl.setopt(pycurl.WRITEFUNCTION, fp.write)
            curl.setopt(pycurl.PROXY, proxy)
            curl.setopt(pycurl.HTTPPROXYTUNNEL,1)
            with self.lock:
				try:
					curl.perform()
					print "res="+proxy+"\tgood"
				except:
					#import traceback
					#traceback.print_exc(file=sys.stderr)
					#sys.stderr.flush()
					print "res="+proxy+"\tbad"
            curl.close()


# Start a bunch of threads
threads = []
for dummy in range(num_conn):
    t = WorkerThread(queue)
    t.start()
    threads.append(t)


# Wait for all threads to finish
for thread in threads:
    thread.join()
