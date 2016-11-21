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
