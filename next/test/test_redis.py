#coding=utf-8
import redis


#pool = 

redis_url = "redis://:zhanghang1003@123.56.16.155:6379/0"
local_url = "redis://:@localhost:6379/0"
redis_cli = redis.StrictRedis


#client = redis_cli.from_url(redis_url)
client = redis_cli.from_url(local_url)
print client.ping()