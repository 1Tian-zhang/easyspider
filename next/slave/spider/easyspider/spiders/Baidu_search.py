#coding=utf-8

from scrapy.spiders import CrawlSpider
from scrapy import Request
import easyspider.rely_tools.tools as tools

#from easyspider.items.Baidu_search_items import Baidu_search_items

"""
针对百度的 web 站点
"""

key_word_file = "./search_key_word.txt"

#query_string = "https://www.baidu.com/s?wd=%s"

query_string = "http://wap.baidu.com/s?word={word}&pu=sz%401321_480&t_noscript=jump&pn={index}"

index_limit = 90


#query_string = "http://wap.baidu.com/s?word=%s&t_noscript=jump"
#$http://wap.baidu.com/s?word=%E4%B8%87%E7%A7%91&t_noscript=jump
#query_string = "http://www.easygot.cn/show_headers.php/?%s"


xpath_search_highlight_title = ""

class Baidu_search(CrawlSpider):
	name = "baidu_search"


	def start_requests(self):
		with open(key_word_file,"r") as f:
			content = map(lambda x:x.strip() , f.readlines())
		#print content
		if not content:
			print "key word file is empty"

		for key_word in content:
			#yield Request(query_string%key_word,callback=self.parse,dont_filter=True)
			yield Request(query_string.format(word=key_word,index=0),callback=self.parse,dont_filter=True,meta={"index":0,"key_word":key_word})

	def parse(self,response):
		search_result = response.xpath("//div[@class=\"resitem\"]")
		

		now_index = response.meta.get("index",0)+10
		key_word = response.meta.get("key_word","未知查询关键字")

		for result in search_result:
			title = "".join(result.xpath("a[@class=\"result_title\"]/div[1]//text()").extract())
			abstract = "".join(result.xpath("a[@class=\"result_title\"]/div[2]//text()").extract())
			url = "http://wap.baidu.com/%s"%result.xpath("a/@href").extract()[0]

			#print "title %s\n abstract %s\n url %s\n"%(title,abstract,url)
			#变原来的 {} 字典，为 Field()
			#crawl_msg = {}
			#crawl_msg = Baidu_search_items()
			crawl_msg = {}
			crawl_msg["search_key_word"] = key_word
			crawl_msg["search_highlight_title"] = title
			crawl_msg["search_highlight_content"] = abstract
			crawl_msg["source_page_url"] = url	
			
			
			yield Request(url,callback=self.parse_source_page,meta={"item":crawl_msg},dont_filter=True)
			#break
			#yield crawl_msg
		# now_index = response.meta.get("index",0)+10
		# key_word = response.meta.get("key_word","未知查询关键字")
		# print query_string.format(word=key_word,index=now_index+10)

		if now_index <= index_limit:
			yield Request(query_string.format(word=key_word,index=now_index+10),callback=self.parse,dont_filter=True,meta={"key_word":key_word,"index":now_index})
		# 	print "next page-------------------------"

	def parse_source_page(self,response):
		item = response.meta.get("item")
		if not item:
			print "with not item............................."
			return 
		item["source_page_content"] = response.body
		yield item