#coding=utf-8
import os
import json
import requests
import time

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
		


def main():
	print detect_online_slave()

if __name__ == '__main__':
	main()