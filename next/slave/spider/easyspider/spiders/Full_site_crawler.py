#coding=utf-8
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy import Request
from easyspider.rely_tools.my import beautify_char

class Full_site_crawler(RedisCrawlSpider):

	name = "full_site_crawler"
	# allowed_domains = ["news.163.com"]
	# start_urls = ["http://news.163.com/"]


	allowed_domains = ["news.cctv.com"]
	start_urls = ["http://news.cctv.com"]


	def start_requests(self):
		for url in self.start_urls:
			yield Request(url,self.parse,dont_filter=True)

	def parse(self,response):
		now_page_content = {}
		now_page_content["source_page_url"] = response.url
		now_page_content["source_page_title"] = beautify_char(",".join(response.xpath("//title//text()").extract())).decode(response.encoding,"ignore")
		#now_page_content["source_page_content"] = response.body.decode("gbk","ignore")
		now_page_content["source_page_content"] = response.body.decode(response.encoding,"ignore")
		yield now_page_content
		next_urls = filter(lambda x:x.endswith("html") or x.endswith("htm") ,response.xpath("//a/@href").extract())
		for url in next_urls:
			yield Request(url,self.parse)