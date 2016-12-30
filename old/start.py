#coding=utf-8
from scrapy.cmdline import execute
print "hello ,i am before than execute"
if __name__ == "__main__":
    execute(['C:\\Software\\python\\Scripts\\scrapy-script.py', 'crawl', 'template_spider','-s','SCHEDULER_FLUSH_ON_START=1'], settings=None)
    #execute(['C:\\Software\\python\\Scripts\\scrapy-script.py', 'crawl', 'Enterprises_msg','-s','SCHEDULER_FLUSH_ON_START=1'], settings=None)
    #execute(['C:\\Software\\python\\Scripts\\scrapy-script.py', 'crawl', 'dmoz'], settings=None)
    #print "ok"
    #execute(['C:\\Software\\python\\Scripts\\scrapy-script.py', 'crawl', 'enterprise_detail'], settings=None)
    
    #execute(['/usr/bin/scrapy', 'crawl', 'template_spider','-s','SCHEDULER_FLUSH_ON_START=1'], settings=None)
    #execute(['/usr/bin/scrapy', 'shell', 'http://www.baidu.com'], settings=None)
    #execute(['/usr/bin/scrapy', 'shell', 'http://www.baidu.com'], settings=None)
    