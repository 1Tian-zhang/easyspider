#coding=utf-8


class Step_records(object):

	def __init__(self,MYSQL_HOST,MYSQL_USER,MYSQL_PASSWORD,RECORD_DB_NAME):
		self.conn = MySQLdb.connect(host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASSWORD,port=3306,charset="utf8")

		self.conn.select_db(MYSQL_DBNAME)
		pass