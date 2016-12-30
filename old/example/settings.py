#coding=utf-8
# Scrapy settings for example project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
SPIDER_MODULES = ['example.spiders']
NEWSPIDER_MODULE = 'example.spiders'

USER_AGENT = 'scrapy-redis (+https://github.com/rolando/scrapy-redis)'

DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

ITEM_PIPELINES = {
    'example.pipelines.ExamplePipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400,
}

DOWNLOADER_MIDDLEWARES = {
	"scrapy.downloadermiddlewares.useragent.UserAgentMiddleware":None,#400
	"example.useragent.UserAgentMiddleware":400,
	#不行
	#"example.middlerwares.useragent.UserAgentMiddleware":400
	#不行
	#"middlerwares.useragent.UserAgentMiddleware":400
	#怎么样都不行...加了个文件夹就进不去了...怀疑是不支持加个文件夹的搜索
	#"a.useragent.UserAgentMiddleware":400
	#"scrapy.downloadmiddlerwares.redirect.RedirectMiddleware":None,
	#"example."
	"scrapy.downloadmiddlewares.redirect.RedirectMiddleware":None,
	"example.redirect.RedirectMiddleware":600



}

COOKIES_ENABLED=True
#COOKIES_ENABLED=False
COOKIES_DEBUG=True

LOG_LEVEL = 'DEBUG'

# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
DOWNLOAD_DELAY = 1

#REDIS_URL = 'redis://123.59.155.25:6379'

#this setting control the threading ,it will be read at the file 
# scrapy/crawler.py/start
#change this num can change the thread,default 10 
REACTOR_THREADPOOL_MAXSIZE=16

#in latest version,web service has been move to another project
#project : scrapy-jsonrpc
#you need to pip install scrapy scrapy-jsonrpc
#WEBSERVICE_ENABLED = True

#EXTENSIONS = {
#    'scrapy_jsonrpc.webservice.WebService': 500,
#}
WEBSERVICE_ENABLED=True
