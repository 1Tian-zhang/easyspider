#coding=utf-8
from my import *
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from gevent.corecext import callback




class ProxySpider(RedisCrawlSpider):
    
    name = "proxy_spider"
    #redis_key = "proxy_spider:start_urls"
    start_urls = ["http://www.xicidaili.com/nn/1"]
    
    
    
    def start_requests(self):
        return RedisCrawlSpider.start_requests(self)
    
    
    def parser_page(self,response):
        pass


    

