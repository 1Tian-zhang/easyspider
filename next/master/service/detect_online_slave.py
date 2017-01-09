#coding=utf-8
import os
import json
import requests
import time
import redis
from background_work.base_redis import BaseRedis


def get_pretty_time():
	return time.strftime("%Y-%m-%d %H:%M:%S")


class Check_online_slave(object):
	def __init__(self,check_online_url="detect_alive",slave_list_file="../../conf/slave_list.json"):

		self.check_online_url = check_online_url
		self.redis = BaseRedis(REDIS_URL)

		slave_list = None
		#---------参数检查--------------------
		flag , result = [True],None
		if not os.path.exists(slave_list_file):
			reason = "slave_list_file not find %s"%slave_list_file
			flag[0] = False
			flag.append("False,%s"%reason)

		if flag[0]:
			try:
				with open(slave_list_file,"r") as f:
					content = json.load(f)
			except Exception,e:
				reason = "read json file error,%s"%e
				flag[0] = False
				flag.append("False,%s"%reason)

			if not content.get("slave_list",0):
				reason = "error:json file have not key slave_list"
				flag[0] = False
				flag.append("False,%s"%reason)
			#---------参数检查--------------------
			slave_list = content.get("slave_list",[])
			#print slave_list
		#print flag,slave_list
		self.init_slave_list(slave_list)
	def run(self):
		while True:
			slave_map = self.redis.hgetall(ONLINE_SLAVE_KEY)[1]	
			self.redis.delete(ONLINE_SLAVE_KEY)
	
			#print slave_map
			online_slave_map = {}
			for salve in slave_map.keys():
				if self.check_response(salve):
					online_slave_map[salve] = get_pretty_time()
			self.redis.hmset(ONLINE_SLAVE_KEY,online_slave_map)
			time.sleep(2)
			#print "time %s checked ,online %s"%(get_pretty_time(),online_slave_map)

	def check_response(self,slave):
		try_time = 3
		url = "http://%s/%s"%(slave,self.check_online_url)
		while try_time:
			try:
				result = requests.get(url)
				if result.status_code == 200:
					#return result
					if result.json()["status"] == 200:
						return True
					return False
			except Exception,e:
				print e
			try_time-=1
			time.sleep(1)
		return False
	def init_slave_list(self,slave_list):
		slave_map = {}
		for slave in slave_list:
			slave_map[slave] = get_pretty_time()

		self.redis.hmset(ONLINE_SLAVE_KEY,slave_map)

	def get_online_slave(self):
		slave_list = self.redis.hgetall(ONLINE_SLAVE_KEY)[1]	
		return slave_list
"""
check_online_url = "detect_alive"

def args_check_get_slave_list(slave_list_file):
	flag , result = [True] , None
	if not os.path.exists(slave_list_file):
		reason = "slave_list_file not find %s"%slave_list_file
		flag[0] = False
		flag.append("False,%s"%reason)

	return flag,result

def get_slave_list(slave_list_file):

	flag ,result = [True] , None
	#---------参数检查--------------------
	if not os.path.exists(slave_list_file):
		reason = "slave_list_file not find %s"%slave_list_file
		flag[0] = False
		flag.append("False,%s"%reason)

	if flag[0]:
		try:
			with open(slave_list_file,"r") as f:
				content = json.load(f)
		except Exception,e:
			reason = "read json file error,%s"%e
			flag[0] = False
			flag.append("False,%s"%reason)

		if not content.get("slave_list",0):
			reason = "error:json file have not key slave_list"
			flag[0] = False
			flag.append("False,%s"%reason)
		#---------参数检查--------------------
		result = content.get("slave_list",[])
	return flag,result



def open_url(url):
	try_time = 3
	while try_time:
		result = requests.get(url)
		if result.status_code == 200:
			return result
		try_time-=1
		time.sleep(2)


def detect_online_slave(slave_list_file="../../conf/slave_list.json"):

	#flag , result = [True],None
	flag , slave_list = get_slave_list(slave_list_file)
#	print flag,slave_list
	if not flag[0]:
		return flag,slave_list

	for slave in slave_list:
		result = open_url("http://%s/%s"%(slave,check_online_url))
		print result.json()

"""

def main():
	Check_online_slave().run()

if __name__ == '__main__':
	main()