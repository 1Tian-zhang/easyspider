#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

"""
crawl_records表
"""
# from scrapy.utils.misc import load_object
# from scrapy.utils.serialize import ScrapyJSONEncoder
# from twisted.internet.threads import deferToThread

import MySQLdb

class Step_records_Middleware(object):

	def __init__(self,MYSQL_HOST,MYSQL_USER,MYSQL_PASSWORD,MYSQL_DBNAME):
		self.conn = MySQLdb.connect(host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASSWORD,port=3306,charset="utf8")
		self.conn.select_db(MYSQL_DBNAME)


	@classmethod
	def from_settings(cls, settings):
	    params = {
	    	"MYSQL_HOST":settings["MYSQL_HOST"],
	    	"MYSQL_USER" : settings["MYSQL_USER"],
			"MYSQL_PASSWORD" : settings["MYSQL_PASSWORD"],
			"MYSQL_DBNAME" : settings["MYSQL_DBNAME"]
	    }
	    return cls(**params)

	@classmethod
	def from_crawler(cls, crawler):
	    return cls.from_settings(crawler.settings)


	def process_response(self,request,response,spider):

		insert_map = {}
		insert_map["url"] = response.url
		insert_map["url_status_code"] = response.status

	

		redirect_urls = request.meta.get("redirect_urls")

		if redirect_urls:
			insert_map["url_history"] = ",".join(redirect_urls)
		else:
			insert_map["url_history"] = "null"
		sql = """
				insert into crawl_records(
					url,
					url_status_code,
					url_history
			)
			values(
					"%(url)s",
					"%(url_status_code)s",
					"%(url_history)s"
			)
		"""

		# if insert_map["url_status_code"] in (301,302,302,304):
		# 	pass
		# else:
		# 	insert_sql = sql%insert_map
		# 	self.db_execute(insert_sql)

		insert_sql = sql%insert_map
		self.db_execute(insert_sql)

		return response


	def db_execute(self,sql):
		cursor = self.conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
		try:
			cursor.execute(sql)
		except Exception,e:
			print "query error and return ",
			print e
			return None
		self.conn.commit()
		cursor.close()



