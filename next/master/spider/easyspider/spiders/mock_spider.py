#coding=utf-8
from scrapy.spiders import CrawlSpider
import scrapy

test_crawl_url = "http://www.easygot.cn/show_headers.php"
#test_crawl_url = "http://www.easygot.cn/mock_302.php"
#test_crawl_url = "http://www.easygot.cn/this_page_id_not_exist.php"
#test_crawl_url = "http://www.easygot.cn/ban_spider.php"

class TestSpider(CrawlSpider):
	name = "mock"
	start_urls = [test_crawl_url for i in range(10)]
	allowed_domain = ["easygot.cn"]
	#start_urls = ["http://www.easygot.cn/show_headers.php","http://www.easygot.cn/show_cookies.php"]
	
	def parse(self,response):
		#@print request.header
		#print response.request.headers
		#print "cookie %s"%response.request.cookies
		print "you are in spider"
		print response.body
		yield scrapy.http.Request(url="http://www.baidu.com",callback=self.parse)