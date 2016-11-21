#coding=utf-8

from scrapy import Request
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
import utils

class TemplateSpider(RedisCrawlSpider):
	name = "template_spider"

	def __init__(self):
		self.controler = utils.Controler("test")
		pass

	def start_requests(self):
		start_urls = self.controler
		for start_url in self.controler.get_start_urls():
			yield Request(start_url,callback=self.discover)
	def discover(self,response):
		#while 
		print response.xpath("//title")[0].extract()	

	
