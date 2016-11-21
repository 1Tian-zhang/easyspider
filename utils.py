#coding=utf-8

from scrapy_redis import get_redis
from my import *
import copy

"""

需要一个类来做以下的事情：

1. 继续解析下一步
2. 从当前步里面可能需要提取信息
3. 记录是从那一步过来的，只需要记录url
所以如果返回下一步的话...干脆不是返回Request 的list
而是返回  类.next_requests_list, 然后再yield

4. 还需要记录自己是第几步，是否是最后一步
5. 同时还需要记录最终的信息，最终的结果  这样子就变成了最终的task 存储所有的信息
"""

class Task(object):
	def __init__(self):
		self.resource_task = None #存储源文件
		self.task_name = None
		self.root_url_type = None
		self.root_url = None
		self.page_step = None
		self.extract_info = None
		
		"""
		extract_info 还需要把step_exrtact 还是 content_page_extract 分析出来

		或者换个方式，直接把内容页，也当作一个步骤页
		"""
	def parse(self,task_name,resource_file="task.json"):
		self.resource_task = self.read_resource_file(task_name,resource_file)
		if self.resource_task:
			self.task_name = self.resource_task["task_name"]
			
			self.root_url_type = self.resource_task["root_info"]["root_url_type"]
			self.root_urls = self.resource_task["root_info"]["root_urls"]

			
			#得不到 page_step 或者是空值
			#if self.page_step.get("page_step"):
			#	self.page_step = None
			
			#self.page_step = self.resource_task["page_step"]
			self.page_step = self.resource_task.get("page_step")


			#self.extract_info = self.resource_task["extract_info"]
			self.extract_info = self.parse_extract_info()

		else:
			
			print "resource task not find"
			exit(-1)
			return None


	def read_resource_file(self,task_name,resource_file):
		try:
			with open(resource_file,"r") as f:
				all_task = json.load(f)
		except IOError,e:
			print e
			return None

		for task in all_task["task"]:
			if task["task_name"] == task_name:
				return task
		return None

	"""
	最终生成
	step_id:how_to_do
	"""
	#def generate_step(self):

	def parse_extract_info(self):
		extract_info = self.resource_task["extract_info"]
		extract_seris = {}
		for extract in extract_info:
			extract_seris[extract["extract_step"]] = extract
		return extract_seris


class Crawl_Log(object):
	
	def __init__(self,task,step):
		self.route_url = []  #是怎么过来的
		self.route_msg = {}  #步骤id : 这一步抓取到的值
		self.is_last_step = False
		self.now_step = step
		self.task = task
		self.crawl_result = {}	
		self.next_url = None
		self.last_step = False
	def add_route_url(self,response):
		self.route_url.append(response.url)

	def generate_next_crawl_log(self,response):

		#self.route_url.append(response.url)
		#如果没有设定page_step 那么就不会产生下一页，直接去extact 了final 下一步
		#if self.task.page_step is None:
		#	return
		#page_step is None
		if not self.task.page_step:
			#由于在调用里面的判断是 if [] 判断的，所以返回空列表比较好
			#return None
			return []
		#step_info is a list
		print "step_info = self.task.page_step[self.now_step-1] and self.now_step-1 is %s"%(self.now_step-1)
		
		"""
		a serious bug
		"""
		try:
			step_info = self.task.page_step[self.now_step-1]
		except Exception,e:
			print "eeeeeeeeeeeeeeeeeeeeeeeeee"
			return []
		#$step_info = self.task.page_step.get(self.now_step-1)
		#if step_info:
		#	return []


		next_url_rule = step_info["next_step_url_rule"]

		if step_info["next_step_url_rule_type"] == "xpath":
			next_url_list = response.xpath(next_url_rule).extract()
		elif step_info["next_step_url_rule_type"] == "regex":
			#re return list so extract is no use
			#next_url_list = response.selector.re(next_url_rule).extract()
			next_url_list = response.selector.re(next_url_rule)


		if step_info.get("extract_index") and isinstance(step_info.get("extract_index"),int):
			next_url_list = [next_url_list[step_info.get("extract_index")]]
		#if step_info["prefix"]:   #有时候没写这个...就出错了
		if step_info.get("prefix"):

			next_url_list = ["%s%s"%(step_info["prefix"],original_url) for original_url in next_url_list]
		#添加一个记录  应该要到第二步了
		self.now_step += 1
		if self.check_is_last_step(step_info):
			self.last_step = True

		#开始复制
		crawl_log_list = []
		for next_url in next_url_list:
			#crawl_log_list.append( copy.deepcopy(sehjklf) )

			self.route_url.append(next_url)

			next_crawl_log = copy.deepcopy(self)
			next_crawl_log.next_url = next_url
			crawl_log_list.append(next_crawl_log)


		"""

		if step_info["next_step_url_rule_type"] == "xpath":
			next_url_rule = step_info["next_step_url_rule"]
			next_url_list = response.xpath(next_url_rule).extract()
			if step_info.get("extract_index") and isinstance(step_info.get("extract_index"),int):
				next_url_list = [next_url_list[step_info.get("extract_index")]]
			#if step_info["prefix"]:   #有时候没写这个...就出错了
			if step_info.get("prefix"):

				next_url_list = ["%s%s"%(step_info["prefix"],original_url) for original_url in next_url_list]
			#添加一个记录  应该要到第二步了
			self.now_step += 1
			if self.check_is_last_step(step_info):
				self.last_step = True

			#开始复制
			crawl_log_list = []
			for next_url in next_url_list:
				#crawl_log_list.append( copy.deepcopy(sehjklf) )

				self.route_url.append(next_url)

				next_crawl_log = copy.deepcopy(self)
				next_crawl_log.next_url = next_url
				crawl_log_list.append(next_crawl_log)

		elif step_info["next_step_url_rule_type"] == "regex":
			next_url_rule = step_info["next_step_url_rule"]
			ext_url_list = response.selector.re(next_url_rule).extract()
			if step_info.get("extract_index") and isinstance(step.get("extract_index"),int):
				next_url_list = [next_url_rule]

		"""
		return crawl_log_list
		#下面就就开始根据有几个next_url 来复制出来

	def generate_request(self):
		pass

	def check_is_last_step(self,step_info):
		#if step_info["last_step"]:  #有些时候没有写last_step  数组访问就会出错
		if step_info.get("last_step"):
			return True
		return False



class Redis_utils(object):
	def __init__(self,**params):
		params = {}
		self.r = get_redis(**params)

	def push_start_urls(self,task_name,urls):
		for url in urls:
			print "%s:%s"%(task_name,"start_urls"),url
			ans_code = self.r.lpush("%s:%s"%(task_name,"start_urls"),url)
	def get_start_urls(self,task_name):
		start_urls = self.r.smembers("%s:%s"%(task_name,"start_urls"))
		return list(start_urls)

	def put_visited_urls(self,task_name,url):
		self.r.sadd("%s:%s"%(task_name,"visited_url"),url)		

	def get_already_exists_urls(self,key_name):
		return self.r.smembers("%s"%key_name)


class Controller(object):
	def __init__(self,task_name,path="task.json"):
		self.task = Task()

		self.task.parse(task_name)
		self.redis = Redis_utils()
	def add_root_url(self):
		print "in add_root_url"
		if self.task.root_url_type == "file":
			#print self.task.root_urls[0]
			root_urls = read_file(self.task.root_urls[0])
		elif self.task.root_url_type == "list":
			root_urls = self.task.root_urls

		print "root_urls is %s"%root_urls

		self.redis.push_start_urls("template_spider",root_urls)

if __name__ == "__main__":
	#u = Controller("ehsy")
	#print "extract_info is %s"%u.task.extract_info
	#u.task.extract_info[2]["detail"]
	#u.add_root_url()
	Controller("enterprise_detail").add_root_url()
