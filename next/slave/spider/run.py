
#coding=utf-8
from scrapy.cmdline import execute
print "hello ,i am before than execute"
if __name__ == "__main__":
    execute(['C:\\Software\\python\\Scripts\\scrapy-script.py', 'crawl', 'template_spider','-s','SCHEDULER_FLUSH_ON_START=1'], settings=None)