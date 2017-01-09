#coding=utf-8

import redis

DEFAULT_REDIS_URL = "redis://:@localhost:6379/0"

master_redis_url = "redis://:zhanghang1003@123.56.16.155:6379/0"

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


class Redis_tools(BaseRedis):
	def test_connection(self):
		print self.redis.ping()


def main():
	base_redis = Redis_tools(master_redis_url)
	#base_redis.test_connection()
	#base_redis.sadd("slave_list", ["testaa","test1","test2","test3"])

	#base_redis.redis.sadd("slave_list", ["testaa","test1","test2","test3"])
	#print base_redis.redis.smembers("slave_list")
	base_redis.hset("online_slave","123.123.123.123","10:00")
	base_redis.hset("online_slave","123.123.123.124","10:01")

	
	print base_redis.hget("online_slave","123.123.123.123")
	print base_redis.hget("online_slave","123.123.123.124")

	base_redis.hmset("online_slave",{"1.1.1.1":"10","2.2.2.2":"30"})

	print base_redis.hgetall("online_slave")

if __name__ == '__main__':
	main()

