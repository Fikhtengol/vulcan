#encoding=utf-8
import re
from urllib import urlopen
import sys
class Filter():
    def __init__(self,_threshold=86,_blocksWidth=3):
        self.threshold=_threshold
        self.blocksWidth=_blocksWidth

    def take_subject(self,html):
        def remove_tag(html):
            #(?is) i忽略大小写，s匹配全部字符包括特殊字符 .*?不贪婪限定符,第一次遇到>就返回
            html = re.sub("(?is)<!DOCTYPE.*?>", "",html)
            html = re.sub("(?is)<!--.*?-->", "",html)
            html = re.sub("(?is)<script.*?>.*?</script>", "",html)
            html = re.sub("(?is)<style.*?>.*?</style>", "",html)
            html = re.sub("&.{2,5};|&#.{2,5};", "",html)
            html = re.sub("(?is)<.*?>", "",html)
            return html

        def take_title():
            titles=re.findall('(?is)<h1.*?>(.*?)</h1>',html)
            if titles:
                title="".join([title for title in titles if title.find("http")==-1])
            else:
                title=""
            return title

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

        title=take_title()
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
                return title,content[0]
            end=get_end(start)
            get_content(start,end)
    
    def pre_process(self,path):
        up=urlopen(path)
        info=up.info()
        html=up.read()
        charset=info.getparam('charset')
        if not charset:
            m=re.search('(?is)<meta.*?charset=(.*?)" />',html)
            if m:charset=m.group(1)
            else:
                print "default charset"
                charset='gb2312'
        html=html.decode(charset,'ignore')
        html.encode('utf-8','ignore')
        return html

    def process(self,path):
        html=self.pre_process(path)
        subject=self.take_subject(html)
        return subject
    
if __name__=="__main__" :
    if len(sys.argv)==2 :
        path=sys.argv[1]
        try:
            fr=Filter()
            subject=fr.process(path)
            print '\n'.join(subject)
            sys.exit(0)
        except Exception,e:
            print e
            raise SystemExit
    print "Usage: %s [path with 'http://' or 'localpath']" % sys.argv[0]
    sys.exit(1)
