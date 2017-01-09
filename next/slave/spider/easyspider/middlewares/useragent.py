#coding=utf-8

from easyspider.rely_tools.UA import *
import random

class UserAgentMiddleware(object):
	print "in UserAgent Middlewareware print hello"
	def __init__(self,user_agent="easyspider"):
		self.UA_headers = UA_headers

	def process_request(self,request,spider):
		this_time_ua = random.choice(self.UA_headers)
		if this_time_ua:
			#print this_time_ua
			request.headers.setdefault("User-Agent",this_time_ua["User-Agent"])