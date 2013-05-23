import re
from urllib import urlopen
import sys
class Filter():
    def __init__(self,_threshold=86,_blocksWidth=3):
        self.threshold=_threshold
        self.blocksWidth=_blocksWidth

    def take_subject(self,html):
        def remove_tag(html):
            html = re.sub("(?is)<!DOCTYPE.*?>", "",html)
            html = re.sub("(?is)<!--.*?-->", "",html)
            html = re.sub("(?is)<script.*?>.*?</script>", "",html)
            html = re.sub("(?is)<style.*?>.*?</style>", "",html)
            html = re.sub("&.{2,5};|&#.{2,5};", "",html)
            html = re.sub("(?is)<.*?>", "",html)
            return html

        def get_start(start):
            for i in range(start,len(blocks)):
                if blocks[i]>self.threshold and blocks[i+1]>0 and blocks[i+2]>0:
                    return i
            return None

        def get_end(start):
            for i in range(start,len(blocks)):
                if blocks[i] == 0 and blocks[i+1] == 0:
                    return i
            return len(blocks)-1

        def get_content(start,end,):
            for i in range(start,end+1):
                content[0]+=lines[i]
                if len(lines[i])<5:continue
                content[0]+='\n'

        content=[""]
        html=remove_tag(html)
        lines=html.split('\n')
        blocks=[]

        lines_len=len(lines)
        blocks.append(0)
        for i in range(self.blocksWidth):
            if i>=lines_len:break
            blocks[0]+=len(lines[i].strip())
            
        start=end=0
        for i in range(1,lines_len-self.blocksWidth):
            blocks.append(blocks[i-1]+len(lines[i+2].strip())-len(lines[i-1].strip()))

        while True:
            start=get_start(end)
            if start==None:
                return content[0]
            end=get_end(start)
            get_content(start,end)

if __name__=="__main__" :
    if len(sys.argv)==2 :
        path=sys.argv[1]
        cmd="open"    
        if path.startswith("http://"):cmd="urlopen"
        try:
            html=eval(cmd)(path).read()
            subject=Filter().take_subject(html)
            print subject
            sys.exit(0)
        except Exception,e:
            print e
            raise SystemExit
    print "Usage: %s [path with 'http://' or 'localpath']" % sys.argv[0]
    sys.exit(1)
