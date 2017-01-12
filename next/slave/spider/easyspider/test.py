# #coding=utf-8

# #import useragent

# #from middlewares import useragent

# #from items.items import ExampleItem

# #print "hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"


# import signal

# # def myHandler(signum,frame):
# # 	print "i received ",signum

# # signal.signal(signal.SIGTSTP,myHandler)

# # signal.pause()

# # print("end of signal demo")



# # signal_names = {}
# # for signame in dir(signal):
# #     if signame.startswith("SIG"):
# #         signum = getattr(signal, signame)
# #         if isinstance(signum, int):
# #             signal_names[signum] = signame

# # print signal_names

# # while True:
# # 	print "Hello,i am test"




# import MySQLdb


# MYSQL_HOST = "123.56.16.155"
# MYSQL_PORT = 3306
# MYSQL_USER = "root"
# MYSQL_PASSWORD = "zhanghang123321"
# MYSQL_DBNAME = "Network_Information_Monitoring"



# class MysqlPipeline(object):

# 	def __init__(self):
# 		self.conn = MySQLdb.connect(host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASSWORD,port=3306,charset="utf8")

# 		self.conn.select_db(MYSQL_DBNAME)
# 		pass

# 	def insert(self):
# 		sql = "insert into from_search_engine(search_key_word) values( '%(search_key_word)s' )"

# 		insert_map = {"search_key_word":"""


# <!DOCTYPE html>
# <html>
# <head>
#     <meta content="always" name="referrer">
#     <script>
#     if (window.parent != window) {
#         window.top.location.replace("http://cc963_710048_beijing.huangye.587766.com/");
#     } else {
#         window.location.replace("http://cc963_710048_beijing.huangye.587766.com/");
#     }
#     </script>
#     <noscript>
#         <META http-equiv="refresh" content="0;URL='http://cc963_710048_beijing.huangye.587766.com/'">
#     </noscript>
# </head>
# <body>
# </body>
# </html>








# 		"""}



# 		#self.db_execute(sql%insert_map)
# 		new_sql = "insert into from_search_engine(search_key_word) values( %s)"
# 		val = ( """aaaaaaaaaaaaaaaa<!DOCTYPE html>
# <html>
# <head>
#     <meta content="always" name="referrer">
#     <script>%
#     if (window.parent != window) {
#         window.top.location.replace("http://cc963_710048_beijing.huangye.587766.com/");
#     } else {
#         window.location.replace("http://cc963_710048_beijing.huangye.587766.com/");
#     }
#     </script>
#     <noscript>
#         <META http-equiv="refresh" content="0;URL='http://cc963_710048_beijing.huangye.587766.com/'">
#     </noscript>
# </head>
# <body>
# </body>
# </html>%""", )


# 		#self.new_db_execute(new_sql,("test"))
# 		self.new_db_execute(new_sql,val)



# # cur.execute("insert into stu_info (name, age, sex) values (%s,%s,%s)", ("Tony",25, "man"))
# # con.commit()

# 	def db_execute(self,sql):
# 		cursor = self.conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
# 		try:
# 			cursor.execute(sql)
# 		except Exception,e:
# 			print "query error and return ",
# 			print e

# 			print "\n\n"
# 			print sql
# 			print "\n\n"
# 			return None
# 		self.conn.commit()
# 		cursor.close()

# 	def new_db_execute(self,sql,val):
# 		cursor = self.conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
# 		try:
# 			cursor.execute(sql,val)
# 		except Exception,e:
# 			print "query error and return ",
# 			print e

# 			print "\n"
# 			print sql
# 			print "\n"
# 			return None
# 		self.conn.commit()
# 		cursor.close()
		
		

# #test = MysqlPipeline()
# #test.insert()


# a = {"a":"b", "c":"d" , "c":"d" , "e":"f" ,"g":"h"}

# #a.keys()


# #print "%s"%a.keys()[0]

# #print "insert into ( %s )"% ",".join(["%s" for i in xrange(len(a.values()))])
# xx = "insert into ( %s )"% ",".join(["%s" for i in xrange(len(a.values()))])
# print xx
# print tuple(a.keys())
# #print xx%a.keys()

# zh = "insert into ( %s,%s,%s,%s )"

# print zh%('a', 'c', 'e', 'g')
# print zh%tuple(a.keys())


# print xx==zh
# print xx%tuple(a.keys())


# print (",".join(["%s" for i in xrange(len(a.values()))]) % tuple(a.keys()) )




# # sql = "insert into table_name(filde) values%s"

# # print  ",".join( ["%s" for i in xrange(len(a)) ] )
# # ans = ",".join( ["%s" for i in xrange(len(a)) ] )
# # print sql % ans

# #print a.items()

# #x = map(lambda x a.items())

# # dict_list = a.items()

# # keys = map(lambda x:x[0] , dict_list)
# # values = map(lambda x:x[1] , dict_list)

# # print dict_list
# # print keys
# # print values

# def join_insert_sql(table_name , insert_map):

# 	sql = "insert into %s(%s) values(%s)"

# 	dict_list = insert_map.items()

# 	keys = tuple( map(lambda x:x[0] , dict_list) )
# 	values = tuple( map(lambda x:x[1] , dict_list) )

# 	sql = sql%(table_name,   (",".join(["%s" for i in xrange(len(a.values()))]) % tuple(a.keys()) )    , ",".join(["%s" for i in xrange(len(values))]))

# 	#print sql
# 	print keys
# 	#print values

# 	return sql , values
# 	# field = zip(insert_map.keys())
# 	# values_field = ",".join( ["%s" for i in xrange(len(insert_map))]  )

# 	# values = zip(insert_map.values())

# 	# print sql%(table_name , field , values_field  )
# 	# print values

# print join_insert_sql("table_name",a)



# # #print a




# # #print zip(a.keys() , a.val())
# # #print zip(a.items())
# # #print a.values()

# # # print zip(a.keys() , a.values())
# # # print tuple(a)
# # # print tuple(a.values())



# # # sql = "insert into %s%s  values%s"




# # # print   [ '%s'  for i in xrange(len(a.values()) ]

# # #print sql%("table_name" , tuple(a) ,   tuple("%s"*a.values())           )




"""
尝试连接跳板机的数据库
"""

import MySQLdb
from sshtunnel import SSHTunnelForwarder


with SSHTunnelForwarder(
	("175.6.5.234",22),
	ssh_username="onlyjump",
	ssh_password=" 23432saW#@Eqwa",
	remote_bind_address=("192.168.10.130",3306)
	) as server:
	conn = MySQLdb.connect(host="127.0.0.1",
		port=server.local_bind_port,
		user="root",
		passwd="B0LLB0LL",
		charset="utf8"
		)


	print conn


	cursor = conn.cursor()

	cursor.execute("show databases;")
	ans = cursor.fetchall()
	print ans


注意要：

self.server.start()

self.server.stop()