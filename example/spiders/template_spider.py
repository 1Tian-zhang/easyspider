#coding=utf-8
from scrapy import Request
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
import utils
import traceback
import json

class TemplateSpider(RedisCrawlSpider):
	name = "template_spider"
	
	#由这里来控制的启动spider，太不方便了...
	#utils.Controller("ehsy").add_root_url()
	utils.Controller("ehsy").add_root_url()


	#task = 

	def __init__(self):
		#注意这里运行了两次...所以造成了本来只有两个链接，却访问了4次
		#self.controller = utils.Controller("ehsy")
		self.controller = utils.Controller("enterprise_detail")
		#parse(task_name)
		#self.controller.add_root_url() 		#添加root_url

	def parse(self,response):
		print "in parse"
		crawl_log = utils.Crawl_Log(self.controller.task,1)

		crawl_log.add_route_url(response)

		if self.controller.task.extract_info.get(crawl_log.now_step):
			self.extract_info(response,crawl_log)

		next_crawl_log_list = crawl_log.generate_next_crawl_log(response)

		if next_crawl_log_list:  #如果能够产生下一页的链接
			for next_crawl_log in next_crawl_log_list:
				print "need to crawl %s"%next_crawl_log.next_url
				yield Request(next_crawl_log.next_url,callback=self.on_page_step,meta={"crawl_log":crawl_log})
		else:  
			self.final_action(crawl_log)
	"""
	#除非多加一个无用的判断最后一页的选项

	调整了规则的话，那么到最后一步就该输出了

	"""
	def on_page_step(self,response):
		#print "on page step"
		crawl_log = response.meta["crawl_log"]

		yield self.extract_info(response,crawl_log)
		if crawl_log.last_step:	#如果为真，那么就结束循环，直接跳到内容页去获取
			#yield self.extract_info(response,crawl_log)  去获取最后一页
			yield self.final_action(crawl_log)
		else:
			#crawl_log.add_router_url(response)  #加入这一部分的路由信息	和 获取到的结果信息
			# 记录工作就留给extract 来做，就不记录了
			next_crawl_log_list = crawl_log.generate_next_crawl_log(response)
			if next_crawl_log_list:   
				for next_crawl_log in next_crawl_log_list:  #第三部，找到那些链接，然后去获取了，所以最后就只要直接调用结束就可以了
					print "start request %s "%next_crawl_log.next_url
					yield Request(next_crawl_log.next_url,callback=self.on_page_step,meta={"crawl_log":crawl_log})
			else:     #找不出来了的，也去解析
				self.final_action(crawl_log) 


	"""
	#觉得这个应该要变成通用的模块，因为不止有内容页需要extract,列表页也要extract
	#根据到底是列表页，还是内容页，来灵活变化
	"""			
	def extract_info(self,response,crawl_log):

		extract_step = crawl_log.now_step
		print type(self.controller.task.extract_info),"extract_info type"
		if self.controller.task.extract_info.get(extract_step):
			extract_rule = self.controller.task.extract_info[extract_step]["detail"]
		else:
			return
		for rule in extract_rule:
			print "rule %s"%rule
			if rule.get("match_type") == "xpath":
				crawl_result = []
				#这里应该是要循环get_val 每个值
				print "rule count %s"%len(rule.get("val"))
				for match_rule in rule.get("val"):
					print "match_rule %s"%match_rule
					xpath_rule = match_rule.get("pattern")
					match_result = response.xpath(xpath_rule).extract()
					print "match_result is %s"%match_result
					print "why not go on ?"
					if isinstance(match_rule["extract_index"],int):
						if match_result:
							match_result = match_result[match_rule["extract_index"]]
					print "match_result now is %s"%match_result
					crawl_result.append(match_result)
    			if rule.get("key"):
    				print crawl_result
    				crawl_log.crawl_result[rule.get("key")] = crawl_result
	def final_action(self,crawl_log):
		try:
			crawl_log.crawl_result["route_url"]=crawl_log.route_url
			with open("crawl_result.txt","a") as f:
				f.write("%s\n"%json.dumps(crawl_log.crawl_result,ensure_ascii=False,indent=2))
		except:
			traceback.print_exc()