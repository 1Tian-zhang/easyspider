#coding=utf-8

import redis



DEFAULT_REDIS_URL = "redis://:@localhost:6379/0"
#master_redis_url = "redis://:zhanghang1003@123.56.16.155:6379/0"
#redis操作类
class BaseRedis(object):

	def __init__(self,redis_url = DEFAULT_REDIS_URL):
		self.redis = redis.StrictRedis.from_url(redis_url)
		if not self.redis.ping():
			print "error,connect redis %s failed"%redis_url

	def sadd(self,key,vals):
		if isinstance(vals,list):
			for val in vals:
				self.redis.sadd(key,val)
		elif isinstance(vals,str):
			self.redis.sadd(key,vals)

	def smembers(self,key):
		flag , result = [True] , None
		try:
			result = self.redis.smembers(key)
		except Exception,e:
			print e
			flag[0] = False
			flag[1] = e
		return flag,result


	def hset(self,area,key,value):
		flag , result = [True],None
		try:
			self.redis.hset(area,key,value)
		except Exception,e:
			print e
			flag[0] = False
			flag.append(e) 
		return flag,result


	def hmset(self,area,mapping):
		flag , result = [True],None
		try:
			self.redis.hmset(area,mapping)
		except Exception,e:
			print e
			flag[0] = False
			flag.append(e) 
		return flag,result

	def hget(self,area,key):
		flag , result = [True],None
		try:
			result = self.redis.hget(area,key)
		except Exception,e:
			print e
			flag[0] = False
			flag.append(e) 
		return flag,result

	def hgetall(self,area):
		flag , result = [True],None
		try:
			result = self.redis.hgetall(area)
		except Exception,e:
			print e
			flag[0] = False
			flag.append(e) 
		return flag,result

	def delete(self,key):
		self.redis.delete(key)


#得到固定格式的时间
def get_pretty_time():
	return time.strftime("%Y-%m-%d %H:%M:%S")