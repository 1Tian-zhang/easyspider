#coding=utf-8
from scrapy.spiders import CrawlSpider


test_crawl_url = "http://www.easygot.cn/show_headers.php"
#test_crawl_url = "http://www.easygot.cn/mock_302.php"


class TestSpider(CrawlSpider):
	name = "test"
	start_urls = [test_crawl_url for i in range(10)]

	#start_urls = ["http://www.easygot.cn/show_headers.php","http://www.easygot.cn/show_cookies.php"]
	
	def parse(self,response):
		#@print request.header
		#print response.request.headers
		#print "cookie %s"%response.request.cookies
		print response.body