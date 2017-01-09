#coding=utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from datetime import datetime

#------模仿scrapy-redis 的pipeline---------------

from scrapy.utils.misc import load_object
from scrapy.utils.serialize import ScrapyJSONEncoder
from twisted.internet.threads import deferToThread

import MySQLdb

#---------------------------


class ExamplePipeline(object):
    def process_item(self, item, spider):
        item["crawled"] = datetime.utcnow()
        item["spider"] = spider.name
        return item

"""
由于mysql 是固定的行列，所以就不太需要引入的 ScrapyJSONEncode

写入mysql的话，一定是有具体的行和列



#mysql 中的文本类型
#TINYTEXT: 256 bytes
#TEXT: 65,535 bytes => ~64kb
#MEDIUMTEXT: 16,777,215 bytes => ~16MB
#LONGTEXT: 4,294,967,295 bytes => ~4GB

create table from_search_engine(
	id bigint(20) unsigned not null ,
	create_time timestamp not null default current_timestamp,
	modify_time timestamp not null default current_timestamp on update current_timestamp,
	
	search_key_word varchar(100) default null,
	search_highlight_title varchar(400) default null,
	search_highlight_content varchar(400) default null,
	search_page_index int default null,
	search_engine tinyint default null,
	
	source_page_title varchar(400) default null,
	source_page_key_word varchar(400) default null,
	source_page_description varchar(400) default null,
	source_page_content mediumtext default null,
	source_page_url varchar(1024) default null,
	source_page_md5 char(32) default null,
	
	primary key(id)
	
)engine=innodb default charset=utf8 comment "从搜索引擎中获取的信息表";


"""

# MYSQL_HOST = "123.56.16.155"
# MYSQL_PORT = 3306
# MYSQL_USER = "root"
# MYSQL_PASSWORD = "zhanghang123321"
# MYSQL_DBNAME = "Network_Information_Monitoring"

class MysqlPipeline(object):

	def __init__(self,MYSQL_HOST,MYSQL_USER,MYSQL_PASSWORD,MYSQL_DBNAME):
		self.conn = MySQLdb.connect(host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASSWORD,port=3306,charset="utf8")

		self.conn.select_db(MYSQL_DBNAME)
		pass



	# @classmethod
	# def from_settings(cls,settings):


	# 	MYSQL_HOST = settings["MYSQL_HOST"]
	# 	MYSQL_PORT = 3306
	# 	MYSQL_USER = settings["MYSQL_USER"]
	# 	MYSQL_PASSWORD = settings["MYSQL_PASSWORD"]
	# 	MYSQL_DBNAME = settings["MYSQL_DBNAME"]


	# 	self.conn = MySQLdb.connect(host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASSWORD,port=3306,charset="utf8")

	# 	self.conn.select_db(MYSQL_DBNAME)


	# @classmethod
	# def from_crawler(cls,crawler):
	# 	return cls.from_settings(crawler.settings)



	@classmethod
	def from_settings(cls, settings):
	    # params = {
	    #     'server': connection.from_settings(settings),
	    # }
	    # if settings.get('REDIS_ITEMS_KEY'):
	    #     params['key'] = settings['REDIS_ITEMS_KEY']
	    # if settings.get('REDIS_ITEMS_SERIALIZER'):
	    #     params['serialize_func'] = load_object(
	    #         settings['REDIS_ITEMS_SERIALIZER']
	    #     )

	    # return cls(**params)

	    params = {
	    	"MYSQL_HOST":settings["MYSQL_HOST"],
	    	"MYSQL_USER" : settings["MYSQL_USER"],
			"MYSQL_PASSWORD" : settings["MYSQL_PASSWORD"],
			"MYSQL_DBNAME" : settings["MYSQL_DBNAME"]

	    }
	    #必须返回一个实例，否则的话，就算启用了也相当于没有使用
	    #这个返回实例就是用到了前面的 init
	    #前面的那个init 是由这个东西来启动的..
	    return cls(**params)
	    pass

	@classmethod
	def from_crawler(cls, crawler):
	    
	    print "\n\n\n in baidu pipeline ,call from crawler,crawler.settings is %s"%crawler.settings.get("HTTPCACHE_STORAGE","没有取到")
	    return cls.from_settings(crawler.settings)


	def process_item(self,item,spider):
		#return deferToThread(self._process_item,item,spider)
		return self._process_item(item,spider)

	def _process_item(self,item,spider):



		insert_map = {}

		insert_map["search_key_word"] = item.get("search_key_word","null")
		insert_map["search_highlight_title"] = item.get("search_highlight_title","null")
		insert_map["search_highlight_content"] = item.get("search_highlight_content","null")
		insert_map["search_engine"] = item.get("search_engine","null")
		insert_map["search_page_index"] = item.get("search_page_index","null")

		insert_map["source_page_title"] = item.get("source_page_title","null")
		insert_map["source_page_key_word"] = item.get("source_page_key_word","null")
		insert_map["source_page_description"] = item.get("source_page_description","null")
		insert_map["source_page_content"] = item.get("source_page_content","null")
		insert_map["source_page_url"] = item.get("source_page_url","null")

		sql = """
				insert into from_search_engine(
					search_key_word,
					search_highlight_title,
					search_highlight_content,
					search_engine,
					search_page_index,

					source_page_title,
					source_page_key_word,
					source_page_description,
					source_page_content,
					source_page_url
			)
			values(
					"%(search_key_word)s",
					"%(search_highlight_title)s",
					"%(search_highlight_content)s",
					"%(search_engine)s",
					"%(search_page_index)s",
					"%(source_page_title)s",
					"%(source_page_key_word)s",
					"%(source_page_description)s",
					"%(source_page_content)s",
					"%(source_page_url)s"
			)


		"""


		insert_sql = sql%insert_map
		
		self.db_execute(insert_sql)
		return item










	def test(self):
		cursor = self.conn.cursor()
		cursor.execute("show tables")
		ans = cursor.fetchall()
		print ans
		cursor.close()


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
		


if __name__ == '__main__':
	MysqlPipeline().test()

	MysqlPipeline()._process_item({"search_key_word":"a"},None)



