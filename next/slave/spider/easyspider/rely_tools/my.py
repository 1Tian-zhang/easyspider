#coding=utf-8
import re,json,os,hashlib,shutil,sqlite3,traceback,random,time,logging,urllib,Queue,threading,multiprocessing,urllib2,cPickle
try:
	import xlrd
except Exception,e:
	print e

try:
	import requests
except Exception,e:
	print e

try:
	import xlwt
except Exception,e:
	print e

try:
	import redis
except Exception,e:
	print e

try:
	import flask
except Exception,e:
	print e


try:
	from bs4 import BeautifulSoup
except Exception,e:
	print e
from UA import *


"""
使用 gevent 一定要单独引入这一个，因为 gevent 要修改python自带的标准库，
启动过程通过monkey patch 完成
"""

try:
	from gevent import monkey; monkey.patch_all()
	import gevent
except Exception,e:
	print e

from functools import wraps
#用来消除，使用装饰器了以后 function.__name__ 变成装饰器名字的问题... #尽管使用了functools的wraps以后，还有一点问题，不过也够用了，不会涉及到出问题的地方

try:
	import MySQLdb
except Exception,e:
	print e

	
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
author = "zhanghang"



"""
屏蔽掉的一个loggging 配置，因为可以在 修饰器里面打印信息，所以就没必要了
"""


logging.basicConfig(level=logging.DEBUG,
					format="%(asctime)s %(levelname)4s: %(message)s",
					datefmt="%Y-%m-%d %H:%M:%S",
					filename="./my.log",
					filemode="w"
					)				
					
					
"""
新建一个StreamHandler,把info 和更高的日志打印到标准输出...并添加
"""
log_console = logging.StreamHandler()
log_console.setLevel(logging.WARN)

format_log_console = logging.Formatter("%(asctime)s %(levelname)s:  %(message)s")
log_console.setFormatter(format_log_console)
logging.getLogger("").addHandler(log_console)

#错误处理装饰器
#这样就不用考虑错误处理的问题了...会自动返回None





def error_solve(fun):
	@wraps(fun)
	def wrapper(*args, **kwargs):
		try:
			ans = fun(*args, **kwargs)  #必须要这一步，不然获取不到返回的信息
			return ans
		except Exception,e:
			info = sys.exc_info()
			ans = traceback.extract_tb(info[2])
			if len(ans)>1:
				
				detail_msg = []
			
				for msg in ans[1:]:
					#这个应该永远用不上，因为不会<4
					if len(msg) >= 4:
						file = msg[0]
						line = msg[1]
						text = msg[3]
						
						if "nt" in os.name:
							file = file.decode()
							text = text.decode()
						detail_msg.append("%s [line:%d] %s"%(file,line,text))
					else:
						detail_msg.append("unbelieveable error !! --> %s"%("".join(msg)))
				print "-----------"		
				logging.error("\t--->\t".join(detail_msg))
			else:
				#print ans
				logging.error("unbelieveable error !! --> %s"%(str(ans[0])))
	return wrapper




"""
读取json文件，把它转化为一个字典返回
"""


@error_solve
def read_json(path):
	if not os.path.isfile(path):
		print "path is not a file"
		return None
	with open(path,"r") as f:
		content = json.load(f)
	return content
	
@error_solve	
def DB_conn(DB_host,DB_user,DB_pwd,DB_name,port=3306):
	try:
		conn = MySQLdb.connect(host=DB_host,user=DB_user,passwd = DB_pwd , charset="utf8" , port=port)
	except Exception,e:
		traceback.print_exc()
	conn.select_db(DB_name)
	return conn

#保留这个直接返回，以适应以前的代码
def DB_query(conn,sql):
	cursor = conn.cursor()
	try:
		cursor.execute(sql)
	except Exception,e:
		print "query error and return ",
		print e
		print sql
		return None
	#这个ans 出来，一样是个元组
	ans = cursor.fetchall()
	conn.commit()
	cursor.close()
	
	if len(ans) == 0:
		return None
	return ans
	
def DB_query_with_head(conn,sql):
	"""
	加上这个，就字段变成了字段名 和 值的对应了，
	{'type': 3, 'name': u'\u6ce2\u65af', 'resources': u'https://img.bwcmall.com/img/default/menu_right_logo_bosi.jpg'}
	不需要 zip 和 dict 不过，还是展示一下这个代码，非常经典
	
	if rs.rows > 0:
		fieldnames = [f[0] for f in rs.fields]
		return [dict(zip(fieldnames, r)) for r in rs.rows]
    else:
		return []
	"""
	cursor = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
	try:
		cursor.execute(sql)
	except Exception,e:
		print "query error and return ",
		print e
		return None
	#这个ans 出来，一样是个元组
	ans = cursor.fetchall()
	conn.commit()
	cursor.close()
	
	if len(ans) == 0:
		return None
	return ans

def DB_execute(conn,sql):
	cursor = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
	try:
		cursor.execute(sql)
	except Exception,e:
		print "query error and return ",
		print e
		return None
	conn.commit()
	cursor.close()
	return True
		
	
#小型md5	
def get_md5(name):
	m = hashlib.md5()
	m.update(name)
	return m.hexdigest()

#复制文件	
def cp(old_path,new_path):
	
	"""
	if not os.path.isdir(old_path):
		print "old_path is not correct dir"

	if not os.path.isdir(new_path):
		print "old_path is not correct dir"
	"""
	try:
		shutil.copy(old_path,new_path)
	except Exception,e:
		print e
		
#新建文件夹，因为os.mkdir()老是喜欢抛出异常实在很烦	
def mk_dir(dir_name):                   
    (lambda dir_name: os.path.exists(dir_name) or os.mkdir(dir_name))(dir_name)

#删除文件夹及里面所有文件
def rm_dir(dir_name):                   
    (lambda dir_name: os.path.exists(dir_name) and shutil.rmtree(dir_name))(dir_name)	
	
#某个文件的大小	返回多少字节
def file_size(path):
	if not os.path.isfile(path):
		print "argv is not a file"
		return None
	return os.path.getsize(path)

	
def DB3_conn(path):
	try:
		conn = sqlite3.connect(path)
	except Exception,e:
		print e
		return None
	return conn
def DB3_query(conn,sql):
	try:
		cursor = conn.cursor()
		cursor.execute(sql)
		#print cursor.description
		ans = cursor.fetchall()
		conn.commit()
	except Exception,e:
		print e
		return None
	return ans
		
def DB3_query_with_head(conn,sql):
	try:
		cursor = conn.cursor()
		cursor.execute(sql)
		#print cursor.description
		head = [t[0] for t in cursor.description]
		content = cursor.fetchall()
		
		ans = [ dict(zip(head,line  )) for line in content]
		
		conn.commit()
	except Exception,e:
		print "error in DB3_query_with_head ",e
		traceback.print_exc()
		return None
	return ans
	
def read_excel(path):
	if not os.path.exists(path):
		print "file %s not exists"%path
		return None
	try:
		wbk = xlrd.open_workbook(path)
		content = []
		for sheet in wbk.sheets():
			context = []
			
			rows = sheet.nrows
			cols = sheet.ncols
			
			for row in xrange(rows):
				line = []
				for col in xrange(cols):
					
					val = sheet.cell(row,col).value
					
					#if cell_type(sheet.cell(row,col)) == 2: #数字类型
					#	val = str(sheet.cell(row,col).value)
					#else:
					#	val = sheet.cell(row,col).value
					#if type(val) 
					#
					# 有时候又确实需要数字类型...只能从逻辑去改
					#
					line.append(val)
				context.append(line)
			content.append(context)
		return content
	except Exception,e:
		traceback.print_exc()
		return None	
		
		
#\u203a  这个就是中文的箭头，也会导致转换错误		
		
def beautify_char(s):
    return re.sub(u"[\\r\\n\\t>\\xa5\\xa0\\xbb\xa9\u203a\xe3 ]","",s)

def beautify_char_with_arrows(s):
    return re.sub(u"[\\r\\n\\t\\xa5 ]","",s)
    
def beautify_char_new(s):
    return re.sub(u"[\\r\\n\\t\\xa5 ]","",s)    
	
	
def read_html(content):
	soup = BeautifulSoup(content,"html.parser")
	return soup


	
	
#根据正则提取网页链接，首先需要open_url 的支持
def extract_link(url,pattern):
	rex = re.compile(pattern)
	r = open_url(url)
	if r is None:
		print "open html failed , return"
		return None
	html = r.content
	results = rex.findall(html,re.S)
	return results
	

	
def make_UA_head(header):   #添加UA头
    if header is None:
		#for UA in UA_headers:
		#	UA['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
		#	UA['Accept-Language']='zh-CN,zh;q=0.8'
		return random.choice(UA_headers)
    else:
		return header	
"""

希望在出现 503 或者 500的时候，自动启用代理
因为status_code 都是数字，所以可以使用  >=500 或者 >=400 来判断

"""

"""
因为使用了 verify = False  所以经常会弹出下面的警告...干脆去它的源码处，注释掉...不要看见它
C:\Software\python\lib\site-packages\requests\packages\urllib3\connectionpool.py:791: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.org/en/latest/security.htm
"""
def open_url(url,header=None,proxy=None,allow_302=True,auth = None,show_error=True):
	header = make_UA_head(header)
	re_try = 3
	while re_try:
		try:
			#print proxy
			r = requests.get(url=url,headers=header,timeout = 5,verify=False,proxies=proxy,allow_redirects=allow_302,auth = auth)
			if r.status_code not in (200,302):
				print "retry because status is %d   url is %s"%(r.status_code,r.url)
				re_try -=1
				continue 
			#print r.text
			#if len(r.content)==0:
				#有时候还存在代理找不到的情况
				#用什么...raise 啊，还要继承异常类，直接用continue 就能继续循环了从此成成成成成成成从此成成粗刺草草成成成成成成
			#	print "len content is 0 status = %d"%r.status_code
			#	continue  
			return r
		except Exception,e:
			print "fail open url %s"%url
			if show_error:
				print e	
			re_try -=1
	return None	


#批量下载图片，读取文本格式：  链接，存储文件名
#应该还可以给个默认的...默认就是链接最后一个 /　这个就可以保证图片的唯一性
#网站名字 + 图片名字  新建一个网站的文件夹，然后把图片放在里面
#注意下载文件里面的内容，实际上，还是调用download_img 实现的，不过统一起来了
def download_img(url,name=None,type="url",sleep=1,path="."):
	#如果只下载单个图片
	if type == "url":
		img = open_url(url)
		
		#如果下载失败...
		if img is None:
			print url
			return False
			
		if name != None:
			with open("%s/%s"%(path,name),"wb") as f:
				f.write(img.content)
		else:
			with open("%s/%s"%(path,url.split("/")[-1].decode().encode("gbk")) ,"wb") as f:
				f.write(img.content)
		return True
	#文件的方式下载
	elif type == "file":
		downlaod_img_file(url,sleep)
	
		
#应该还可以给个默认的...默认就是链接最后一个 /　这个就可以保证图片的唯一性		
def downlaod_img_file(file_name,sleep):
	with open(file_name,"r") as f:
		content = map(lambda x:x.strip(),f.readlines())
	
	
	#可能一个文件里面，有多个不同的网址...所以每个都要比较一下，要不要新建
	#img_path = content[0].split("/")[2]
	#mk_dir(path)
	
	rate = 1
	all = len(content)
	
	failed = []
	
	for line in content:
		#过滤有些为空的行
		if "http" not in line:
			continue
		img_path = line.split("/")[2]
		mk_dir(img_path)
		
		ans = download_img(line,path=img_path)
		if ans:
			print "[%d / %d] , ok "%(rate,all)
		else:
			print "failed ! [%d / %d]"%(rate,all)
			failed.append(line)
		rate+=1
		time.sleep(random.randint(0,sleep))
		
	if failed != []:
		print "failed %d , url in img_filed.txt"%len(failed)
		with open("img_failed.txt","w") as f:
			f.write("\n".join(failed))
	else:
		print "all ok"

@error_solve
def urlencode(url):
	return urllib.urlencode({"url":url}).split("=")[1]
	
@error_solve
def urldecode(url):
	return urllib.unquote(url)	
		
@error_solve
def read_file(path):
	if os.path.exists(path):
		with open(path,"r") as f:
			content = map(lambda x:x.strip(),f.readlines())
		return content
	else:
		logging.error("file not exists")
		return None


def get_time():
	return time.strftime("%Y-%m-%d %H:%M:%S")


"""
#用类，是因为这个要保持数据库连接...总不能一引入my包就保持数据库连接吧
#而python中又没有 static 全局变量 所以用类保存一下链接状态，
class Proxy(object):
	def __init__(self,host="localhost",user="root",pwd="",name="proxy"):	
		self.conn = DB_conn(host,user,pwd,name)
		self.query_sql = "select url from proxy_table where type='%s'"
		self.del_sql = "delete from proxy_table where md5=%s"
	def get_proxy(self,type="http"):
		proxy = DB_query_with_head(self.conn,self.query_sql%type)
		#让选择，变成随机选择
		if proxy is not None:
			all = len(proxy)
			return proxy[random.randint(0,all-1)]["url"]
		else:
			return None
	def del_proxy(self,proxy):
		md5_proxy = get_md5(proxy)
		DB_execute(self.conn,sele.del_sql%md5_proxy)

"""
		
class Write_Excel():
	def __init__(self):
		self.wbk = xlwt.Workbook(encoding="utf-8")
		self.sheet = self.wbk.add_sheet("ans",cell_overwrite_ok=True)
	
	
	def write(self,row,line,sheet=None):
		if sheet is None:
			for col in xrange(len(line)):
				self.sheet.write(row,col,line[col])
	
	def save(self,name="ans.xls"):
		try:
			self.wbk.save(name)
		except Exception,e:
			print e
		return None

"""
心疼，重复了这么多....写了好多 insert 和 values
"""
#self.insert_supplier_sql = "insert into bc_supplier%s values%s"
#self.insert_supplier_brand_sql = "insert into bc_supplier_brand%s values%s"
#self.insert_supplier_warehouse_sql = "insert into bc_supplier_warehouse%s values%s"
#self.insert_brand_sql = "insert into bp_brand%s values%s"		
#insert into %s%s values 想要实现这样子的效果，表名也是可以自定义，真的不好实现
#有这功夫，不如多写上一行
#test case: join_sql("insert into crawl_url%s values%s;",{"url":"baidu","status":1})		
def join_sql(template_sql , sql_map,table_name=None,split_symbol='"'):
	try:
		"""
		会有这样的问题： cheuk's  这样本身名字带有了单引号的 会报错，会导致单引号提前结束....
		
		"""
		#form_list=[[ "`%s`"%k,"'%s'"%v] for k,v in sql_map.items()]
		if split_symbol == '"':
			form_list=[[ "`%s`"%k,'"%s"'%v] for k,v in sql_map.items()]
		
		elif split_symbol == "'":
			form_list=[[ "`%s`"%k,"'%s'"%v] for k,v in sql_map.items()]
		key = [ i[0] for i in form_list]
		val = [ i[1] for i in form_list]
		if table_name is not None:
			sql = template_sql%(table_name, "(%s)"%(",".join(key)),"(%s)"%(",".join(val)))
		else:
			sql = template_sql%("(%s)"%(",".join(key)),"(%s)"%(",".join(val)))
		return sql
	except Exception,e:
		traceback.print_exc()
		print table_name
		print "join sql error , please check"
	return None

	
	
"""
代理整合
"""	
"""

数据库表结构

drop table if exists `proxy_table`;
create table proxy_table(id int(15) auto_increment,
create_time timestamp,
last_modify_time timestamp,
proxy varchar(20),
type varchar(6),
check_num int(10),
region varchar(50),
last_used_time timestamp,
md5_proxy varchar(50),
primary key (id,md5_proxy)
)engine=InnoDB charset=UTF8;

"""

def call_control_consumer(fn):
	@wraps(fn)
	def wrapper(*args,**kwargs):
		while True:
			print args
			print "start comsumer"
			fn(*args,**kwargs)
			time.sleep(10)
	return wrapper



def call_control_producer(fn):
	@wraps(fn)
	def wrapper(*args,**kwargs):
		while True:
			print "start_call "
			fn(*args,**kwargs)
			time.sleep(1)
	return wrapper

"""
后面发现，存在一个重复检测的问题。因为启动多个线程的时候，每个都去拿，这样子肯定是重复的拿到同一批数据
所以无论多少个线程去操作，都变成了是同一个线程来检测多次
想要改变这种情况...要么是
1. 增加是否被取走的字段
2. 只开一个线程，但是这个线程里面的分为gevent去访问，内部分为 gevent 去访问，这样子也能达到避免重复的效果。而且只需
启动一个实例，然后基础的数据库结构也不用怎么去修改
"""
#老版本是单线程，切换成多进程
class Proxy_old(object):
		def __init__(self,type="producer"):
		    DB_host = "localhost"
		    DB_user = "root"
		    DB_passwd = ""
		    DB_name = "proxy"
		    
		    self.type = type.lower()
		    self.conn = DB_conn(DB_host,DB_user,DB_passwd,DB_name)
		    
		    if self.type == "producer":
		        self.http_api  = "http://dev.kuaidaili.com/api/getproxy/?orderid=927134582586035&num=100&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=1&an_an=1&an_ha=1&sp2=1&quality=1&sep=2"
		        self.https_api = "http://dev.kuaidaili.com/api/getproxy/?orderid=927134582586035&num=100&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=2&method=1&an_an=1&an_ha=1&sp2=1&quality=1&sep=2"
		        self.insert_sql = "insert into proxy_table(`create_time`,`proxy`,`type`,`check_num`,md5_proxy) values('%(create_time)s','%(proxy)s','%(type)s',0,'%(md5_proxy)s');"
		        self.query_sql = "select md5_proxy from proxy_table"
		    
		    elif self.type == "consumer":
		        self.http_check = "http://1212.ip138.com/ic.asp"
		        self.https_check = "https://geoiptool.com/zh/"
		        self.query_sql = "select id,proxy,type from proxy_table where type='%s' order by check_num asc limit 100"
		        self.update_sql = "update proxy_table set last_modify_time = '%(last_modify_time)s',region ='%(region)s',check_num = check_num+1 where id = %(id)d;"
		        self.delete_sql = "delete from proxy_table where id = %(id)d;"
		        
		def run(self,id):
			print id
			#gevent.sleep(1)
			if self.type == "producer":
				self.producer()
			elif self.type == "consumer":
				self.consumer()
		@call_control_producer		
		def producer(self):
			http_list = self.get_proxy("http")
			https_list = self.get_proxy("https")
			self.insert_proxy(http_list)
			self.insert_proxy(https_list)
			
		def get_proxy(self,get_type="http"):
			get_type = get_type.lower()
			if get_type == "http":
				proxys = open_url(self.http_api)
			elif get_type == "https":
				proxys = open_url(self.https_api)
			return map(lambda proxy:{get_type:proxy} , proxys.content.split("\n"))
		
		def insert_proxy(self,proxy_list):
			try:
				#要全部变成字典的形式，下面注释的，是有[] 列表 + 字典的形式
				#already_haved = map(lambda md5_proxy:{md5_proxy:1} ,list(DB_query(self.conn,self.query_sql)))
				already_haved = {}
				for md5_proxy in DB_query(self.conn,self.query_sql):
						already_haved[md5_proxy[0]]=1   #不加0的话，就变成了元组...就不能去匹配了
				#print already_haved
				#time.sleep(5)
			except Exception,e:
				already_haved = {"":""} #出现这种情况，是因为数据库里面没有东西
			for current_proxy in proxy_list:
				proxy_type , proxy = current_proxy.items()[0]
				md5_proxy = get_md5("%s%s"%(proxy_type,proxy))
				if already_haved.get(md5_proxy,0):
					print "already have , skip"
					#time.sleep(30)	
					continue
				else:
					insert_map = {"create_time":get_time() , "proxy" : proxy,"type":proxy_type,"md5_proxy":md5_proxy}
					print self.insert_sql%(insert_map)
					DB_execute(self.conn,self.insert_sql%(insert_map))
		#@call_control_consumer
		def consumer(self):
			proxy_map = self.take_out_proxy()
			for id,val in proxy_map.items():
				region = self.check_proxy(val)
				if region is not None:
					self.update_proxy(id,region)
				else:
					self.delete_proxy(id)
				
		def take_out_proxy(self):
			proxy_list = []
			while proxy_list == []:
				try:
					proxy_list = list(DB_query(self.conn,self.query_sql%("http")))    
					proxy_list.extend(list(DB_query(self.conn,self.query_sql%("https"))))
				except Exception,e:
					#print e	
					pass
			#这样子做，就变成了一个 列表的字典了
			#a = map(lambda proxy:{proxy[0]:[proxy[2],proxy[1]]} , proxy_list)
			#print a
			#return map(lambda proxy:{proxy[0]:[proxy[2],proxy[1]]} , proxy_list)
			proxy_map = {}
			for line in proxy_list:
				proxy_map[line[0]] = [line[2],line[1]]
			return proxy_map
		  
		def check_proxy(self,val):
			if val[0] == "http":
				r = open_url(self.http_check,proxy={val[0]:val[1]},show_error=False)
			elif val[0] == "https":
				r = open_url(self.https_check,proxy={val[0]:val[1]},show_error=False)
			if r is not None:
				region = self.get_region(r,val[0])
				return region
			return None
				
		def get_region(self,r,type):
			soup = read_html(r.content)
			region = None
			if type == "http":
				try:
					region = beautify_char(soup.find_all("center")[0].text)
				except Exception,e:
					pass
			elif type == "https":
				try:
					region = beautify_char(soup.find_all("div",class_="sidebar-data hidden-xs hidden-sm")[0].find_all("div")[5].find_all("span")[1].text)
				except Exception,e:
					pass
			#让出错处理，全部让修饰器来做
			return region
		
		def update_proxy(self,id,region):
			update_map = {"id":id , "region":beautify_char(region),"last_modify_time":get_time()}
			print self.update_sql%update_map
			DB_execute(self.conn,self.update_sql%update_map)
			
		def delete_proxy(self,id):
			delete_map = {"id":id}
			DB_execute(self.conn,self.delete_sql%delete_map)
		def test():
			pass	
	
		def free_proxy_kuaidaili(self):
			pass
			
			
			
class Proxy(object):
		def __init__(self,type="producer"):
		    DB_host = "localhost"
		    DB_user = "root"
		    DB_passwd = ""
		    DB_name = "proxy"
		    
		    self.type = type.lower()
		    self.conn = DB_conn(DB_host,DB_user,DB_passwd,DB_name)
		    
		    if self.type == "producer":
		        self.http_api  = "http://dev.kuaidaili.com/api/getproxy/?orderid=927134582586035&num=100&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=1&an_an=1&an_ha=1&sp2=1&quality=1&sep=2"
		        self.https_api = "http://dev.kuaidaili.com/api/getproxy/?orderid=927134582586035&num=100&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=2&method=1&an_an=1&an_ha=1&sp2=1&quality=1&sep=2"
		        self.insert_sql = "insert into proxy_table(`create_time`,`proxy`,`type`,`check_num`,md5_proxy) values('%(create_time)s','%(proxy)s','%(type)s',0,'%(md5_proxy)s');"
		        self.query_sql = "select md5_proxy from proxy_table"
		    
		    elif self.type == "consumer":
		        self.http_check = "http://1212.ip138.com/ic.asp"
		        self.https_check = "https://geoiptool.com/zh/"
		        self.query_sql = "select id,proxy,type from proxy_table where type='%s' order by check_num asc limit 100"
		        self.update_sql = "update proxy_table set last_modify_time = '%(last_modify_time)s',region ='%(region)s',check_num = check_num+1 where id = %(id)d;"
		        self.delete_sql = "delete from proxy_table where id = %(id)d;"
		        
		def run(self,id):
			print id
			gevent.sleep(1)
			if self.type == "producer":
				self.producer()
			elif self.type == "consumer":
				self.consumer()
		@call_control_producer		
		def producer(self):
			http_list = self.get_proxy("http")
			https_list = self.get_proxy("https")
			self.insert_proxy(http_list)
			self.insert_proxy(https_list)
			
		def get_proxy(self,get_type="http"):
			get_type = get_type.lower()
			if get_type == "http":
				proxys = open_url(self.http_api)
			elif get_type == "https":
				proxys = open_url(self.https_api)
			return map(lambda proxy:{get_type:proxy} , proxys.content.split("\n"))
		
		def insert_proxy(self,proxy_list):
			try:
				#要全部变成字典的形式，下面注释的，是有[] 列表 + 字典的形式
				#already_haved = map(lambda md5_proxy:{md5_proxy:1} ,list(DB_query(self.conn,self.query_sql)))
				already_haved = {}
				for md5_proxy in DB_query(self.conn,self.query_sql):
						already_haved[md5_proxy[0]]=1   #不加0的话，就变成了元组...就不能去匹配了
				#print already_haved
				#time.sleep(5)
			except Exception,e:
				already_haved = {"":""} #出现这种情况，是因为数据库里面没有东西
			for current_proxy in proxy_list:
				proxy_type , proxy = current_proxy.items()[0]
				md5_proxy = get_md5("%s%s"%(proxy_type,proxy))
				if already_haved.get(md5_proxy,0):
					print "already have , skip"
					#time.sleep(30)	
					continue
				else:
					insert_map = {"create_time":get_time() , "proxy" : proxy,"type":proxy_type,"md5_proxy":md5_proxy}
					print self.insert_sql%(insert_map)
					DB_execute(self.conn,self.insert_sql%(insert_map))
		@call_control_consumer
		def consumer(self):
			#转换成线程安全的队列
			self.q = Queue.Queue()
			#print self.take_out_proxy()
			#exit(0)
			map(lambda item:self.q.put(item) , list(self.take_out_proxy().items()))
			print self.q.qsize()
			gevent.joinall([
				gevent.spawn(self.gevent_check_proxy)
				for i in range(1000)
			])
			
			
		def gevent_check_proxy(self):
			print "in gevent"
			while True:
				try:
					item = self.q.get(timeout=2)
				except Exception,e:
					print e
					return
				#print item
				id , val = item[0],item[1]
				region = self.check_proxy(val)
				if region is not None:
					self.update_proxy(id,region)
				else:
					self.delete_proxy(id)
			"""
			proxy_map = self.take_out_proxy()
			for id,val in proxy_map.items():
				region = self.check_proxy(val)
				if region is not None:
					self.update_proxy(id,region)
				else:
					self.delete_proxy(id)
			"""	
		def take_out_proxy(self):
			proxy_list = []
			while proxy_list == []:
				try:
					proxy_list = list(DB_query(self.conn,self.query_sql%("http")))    
					"""
					先不检查 https
					"""
					#proxy_list.extend(list(DB_query(self.conn,self.query_sql%("https"))))
				except Exception,e:
					#print e	
					pass
			#这样子做，就变成了一个 列表的字典了
			#a = map(lambda proxy:{proxy[0]:[proxy[2],proxy[1]]} , proxy_list)
			#print a
			#return map(lambda proxy:{proxy[0]:[proxy[2],proxy[1]]} , proxy_list)
			proxy_map = {}
			for line in proxy_list:
				proxy_map[line[0]] = [line[2],line[1]]
			return proxy_map
		  
		def check_proxy(self,val):
			if val[0] == "http":
				r = open_url(self.http_check,proxy={val[0]:val[1]},show_error=False)
			elif val[0] == "https":
				r = open_url(self.https_check,proxy={val[0]:val[1]},show_error=False)
			if r is not None:
				region = self.get_region(r,val[0])
				return region
			return None
				
		def get_region(self,r,type):
			soup = read_html(r.content)
			region = None
			if type == "http":
				try:
					region = beautify_char(soup.find_all("center")[0].text)
				except Exception,e:
					pass
			elif type == "https":
				try:
					region = beautify_char(soup.find_all("div",class_="sidebar-data hidden-xs hidden-sm")[0].find_all("div")[5].find_all("span")[1].text)
				except Exception,e:
					pass
			#让出错处理，全部让修饰器来做
			return region
		
		def update_proxy(self,id,region):
			update_map = {"id":id , "region":beautify_char(region),"last_modify_time":get_time()}
			print self.update_sql%update_map
			DB_execute(self.conn,self.update_sql%update_map)
			
		def delete_proxy(self,id):
			delete_map = {"id":id}
			DB_execute(self.conn,self.delete_sql%delete_map)
		def test(self):
			pass	
		
		
		#这样方便以后添加规则
		
		"""
		Traceback (most recent call last):
		  File "免费代理.py", line 6, in <module>
			a.free_run()
		  File "C:\Software\python\lib\my.py", line 850, in free_run
			for i in range(10)
		  File "C:\Software\python\lib\site-packages\gevent\greenlet.py", line 631, in joinall
			return wait(greenlets, timeout=timeout, count=count)
		  File "C:\Software\python\lib\site-packages\gevent\hub.py", line 1014, in wait
			return list(iwait(objects, timeout, count))
		  File "C:\Software\python\lib\site-packages\gevent\hub.py", line 958, in iwait
			obj.rawlink(switch)
		AttributeError: 'NoneType' object has no attribute 'rawlink'
		请按任意键继续. . .
		"""
		
		def free_run(self):
			#self.free_start_urls = self.get_free_url_rule()
			#添加到队列里面
			self.free_q = Queue.Queue()
			map(lambda url:self.free_q.put(url) ,self.get_free_url_rule())
			#然后再一个个的去解决
			task_list = [ gevent.spawn(self.solve_free_proxy) for i in range(10)]
			#print task_list
			#gevent.joinall([
			#	self.solve_free_proxy
			#	 for i in range(10)
			#])
			
			gevent.joinall(task_list)
		
		#要是字典，才好分析出来是那个网站，对应出规则
		"""
		
		这里可以控制，抓取那个网站
		
		
		"""
		
		def get_free_url_rule(self):
			free_urls = []
			#free_urls.extend(self.free_kuaidaili_url_rule())
			#这样就可以随时多加一个
			free_urls.extend(self.free_xici_url_rule())
			
			return free_urls
		def free_kuaidaili_url_rule(self):
			free_type = "kdl"
			url = "http://www.kuaidaili.com/free/inha/%d"
			urls = [{free_type : url%num} for num in xrange(1,1000+1)]
			return urls
		
		def free_xici_url_rule(self):
			free_type = "xici"
			url = "http://www.xicidaili.com/nn/%d"
			urls = [{free_type : url%num} for num in xrange(1,1000+1)]
			return urls
		
		def solve_free_proxy(self):
			#print 1
			#return
		
			while True:
				try:
					item = self.free_q.get(timeout=2)
				except Exception,e:
					print e
					return
				#print item
				url_type , url = item.items()[0]
				
				r = open_url(url)
				if r is None:
					continue
				
				#开始对每个特殊网站有单独的处理规则
				#返回的是 {type:proxy}
				proxys_list = []
				if url_type == "kdl":
					proxy_list = self.extract_kuaidaili_proxy(r)
					#print proxy_list
					self.insert_proxy(proxy_list)
				elif url_type == "xici":
					proxy_list = self.extract_xici_proxy(r)
					self.insert_proxy(proxy_list)
		
		def extract_kuaidaili_proxy(self,r):
			urls_list = []
			try:
				soup = read_html(r.content)
				table = soup.find_all("table",class_="table table-bordered table-striped")[0]
				
				for tr in table.find_all("tr")[1:]:
					ip = tr.find_all("td")[0].text
					port = tr.find_all("td")[1].text
					proxy_type = "https" if "https" in tr.find_all("td")[3].text else "http"
					urls_list.append({proxy_type:"%s:%s"%(ip,port)})
			except Exception,e:
				print e
			return urls_list
				
		def extract_xici_proxy(self,r):
			urls_list = []
			try:
				soup = read_html(r.content)
				table = soup.find_all("table",id="ip_list")[0]
				
				for tr in table.find_all("tr")[1:]:
					ip = tr.find_all("td")[1].text
					port = tr.find_all("td")[2].text
					proxy_type = "https" if "https" in tr.find_all("td")[5].text else "http"
					urls_list.append({proxy_type:"%s:%s"%(ip,port)})
			except Exception,e:
				print e
			return urls_list
		
		def da_xiang_proxy(self):
			#self.da_xiang_proxy_q = Queue.Queue()
			#da_xiang_http_api = "http://tpv.daxiangip.com/ip/?tid=558136305087216&num=49999&delay=3&filter=on"
            #proxy_table = [{"http":"http://%s"%line} for line in open_url(da_xiang_http_api).content.split("\r\n")]
            #map(self.proxy_q.put,proxy_table) 
 			pass


		"""
		还是得设计了再写啊...
		
		def free_proxy_kuaidaili(self):
			self.free_kdl_url = "http://www.kuaidaili.com/free/inha/%d"
			self.free_kdl_q = Queue.Queue()
			map(lambda url:self.free_kdl_q.put(url), [self.free_kdl_url%num for num in xrange(1,1000+1)] )
			gevent.joinall([
				gevent.spawn(self.solve_free_kuaidaili)
				for i in range(10)
			])
		def solve_free_kuaidaili(self):
			while True:
				try:
					url = self.free_kdl_q.get(timeout=2)
				except Exception,e:
					print e
					return
				self.extract
		"""
"""

断点抓取

"""

"""

建库语句
create table crawl_urls(id int(15) auto_increment , 
create_time timestamp,
modify_time timestamp,
url varchar(300),
md5_url varchar(40),
status TINYINT,   #0 是未抓取    1是成功  2是已经取走
spider_name varchar(100),
primary key(id,md5_url),
UNIQUE key (md5_url)
)engine=INNODB charset=utf8


当时的测试代码


	a = Crawl_url()
	a.dump(read_file("urls.txt"),"test_spider")
	#a.clean("test_spider")
	
	#while True:
	#	ans = a.load("test_spider")
	#	print "\n".join(ans)
	#	time.sleep(1)
	

"""
class Crawl_url(object):
	def __init__(self,DB_host="localhost",DB_user="root",DB_passwd="",DB_name="crawl_url_record"):
		self.conn = DB_conn(DB_host,DB_user,DB_passwd,DB_name)
		if self.conn is None:
			print "error ! can not cnnect db"
			exit(-2)
		self.dump_sql = "insert into crawl_urls%s values%s"
		self.load_sql = "select url from crawl_urls where spider_name = '%s' and status=0 limit %s"
		self.sign_sql = "update crawl_urls set status=2 where md5_url='%s'"  #拿走时候的标记
		self.success_sql = "update crawl urls set status=1 where md5_url='%s'" #成功
		#self.clean_sql = "update crawl_urls set status=0 where id=%s" #清理拿走但是没有成功的url
		self.clean_sql = "update crawl_urls set status=0 where spider_name='%s' and status=2"
		self.delete_sql = "delete from crawl_urls where id = %s" #全部完成后，删除成功的url
		
	def dump(self,content,spider_name):
		for url in content:
			url_map = {}
			url_map["create_time"]=get_time()
			url_map["url"] = url
			url_map["md5_url"] = get_md5("%s%s"%(spider_name,url))
			url_map["status"] = 0
			url_map["spider_name"] = spider_name
			#print url_map
			#print join_sql(self.dump_sql,url_map)
			print url
			if DB_execute(self.conn,join_sql(self.dump_sql,url_map)) is None:
				print "url %s dump failed"%url
	def load(self,spider_name,take_num=100):
		urls = DB_query(self.conn,self.load_sql%(spider_name,take_num))
		if urls is None:
			print "load error ! please check"
			return None
		ans = []
		for url in urls:
			if DB_execute(self.conn,self.sign_sql%(get_md5("%s%s"%(spider_name,url[0])))) is None:
				print "url %s sign error !"%url
			ans.append(url[0])
		return ans
	def success(self,url):
		if DB_execute(self.conn,self.success_sql%get_md5(url)) is None:
			print "url can't success ,please check"%url
	
	def clean(self,spider_name,max_time=None):
		if DB_execute(self.conn,self.clean_sql%spider_name) is None:
			print "url can't success ,please check"%url	
			
			
			
			
			
#有参数的函数怎么办，不知道 暂时不考虑	
def run_with_gevent(task,num):
	gevent.joinall([
	gevent.spawn(task) for i in xrange(num)
	])
	

#关于传入的data,只要传入字典就好了
#自动的转成json
#注意要返回状态码变成201 已处理才是对的
def http_put(url,data=None):
	r = None
	try:
		if isinstance(data,dict) is False:
			print "data is not dict,return and check"
			return
		data = json.dumps(data)
		try:
			#print data
			pass
		except:
			pass
		r = requests.put(url,data,timeout=3)
	except Exception,e:
		traceback.print_exc()
	return r