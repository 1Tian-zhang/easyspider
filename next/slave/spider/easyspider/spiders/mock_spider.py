#coding=utf-8
from scrapy.spiders import CrawlSpider
import scrapy
import time
from scrapy import Request

from easyspider.items.Baidu_search_items import Baidu_search_items

#import easyspider.test

test_crawl_url = "http://www.easygot.cn/show_headers.php"
#test_crawl_url = "http://www.easygot.cn/mock_302.php"
#test_crawl_url = "http://www.easygot.cn/this_page_id_not_exist.php"
#test_crawl_url = "http://www.easygot.cn/ban_spider.php"

index_limit = 20

class TestSpider(CrawlSpider):
	name = "mock"
	start_urls = [test_crawl_url for i in range(1000000)]
	#start_urls = [test_crawl_url ]
	allowed_domain = ["easygot.cn"]
	#start_urls = ["http://www.easygot.cn/show_headers.php","http://www.easygot.cn/show_cookies.php"]
	
	def start_requests(self):
		for url in self.start_urls:
			yield Request(url,meta={"index":0},dont_filter=True)

	def parse(self,response):
		#@print request.header
		#print response.request.headers
		#print "cookie %s"%response.request.cookies
		print "you are in spider"
		#print response.body
		#yield scrapy.http.Request(url="http://www.baidu.com",callback=self.parse)
		
		now_index = response.meta.get("index",0)+10
		print now_index , now_index<=index_limit

		item = Baidu_search_items()

		item["search_key_word"] = "now all changed "

		# yield {
		# 	"time":time.ctime(),
		# 	"url":response.url,
		# 	"name":"i am  now asdasd",
		# 	"search_key_word":"mock"
		# }

		yield item

		if now_index <= index_limit:
			yield Request(test_crawl_url,callback=self.parse,meta={"index":now_index},dont_filter=True)
		#return {
		# 	"time":time.ctime(),
		# 	"url":response.url
		# }

