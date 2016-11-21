#coding=utf-8
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from scrapy_redis.spiders import RedisCrawlSpider


class MyCrawler(RedisCrawlSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'zk360'
    redis_key = 'test:zk360'

    rules = (
        # follow all links
        Rule(LinkExtractor(allow=("brand\.php?id="),), callback='parse_page', follow=True),
		Rule(LinkExtractor(), callback='parse_page', follow=True),
    )

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(MyCrawler, self).__init__(*args, **kwargs)

    def parse_page(self, response):
        print "yyyyyyyyyyyyyyyyyy"
        print response.url
		#return {
        #    'name': response.css('title::text').extract_first(),
        #    'url': response.url,
        #}