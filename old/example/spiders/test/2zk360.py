from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class DmozSpider(CrawlSpider):
    """Follow categories and extract links."""
    name = 'zk360'
    allowed_domains = ['zkh360.com']
    start_urls = ['http://www.zkh360.com/Brand/Index/?catalog_id=&firstLetter=%E5%85%A8%E9%83%A8']
    
    rules = [
       Rule(LinkExtractor(allow=("/zkh_catalog"),), callback='parse_directory', follow=True)
    ]

    def parse_directory(self, response):
        print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        print response.url
        yield {"name":response.url}