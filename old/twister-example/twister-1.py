#coding=utf-8

import argparse,socket

"""
一台机器开启一个端口发送消息，然后另外一边用　telnet 来接收
"""


def parse_args():
	parser = argparse.ArgumentParser()
	args = parser.parse_args()


"""
listen 里面是允许的最大在线数目

socket.listen(backlog)
Listen for connections made to the socket. The backlog argument specifies the maximum number of queued connections and should be at least 0; the maximum value is system-dependent (usually 5), the minimum value is forced to 0.
"""

def main():
	#创建TCP socket 可以不写默认参数，默认就是TCP socket
	# tcp_socket = socket.socket()

	# tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# tcp_socket.bind(('',10000))
	# tcp_socket.listen(10)

	# #print "socket.getsocketname is %s"%(tcp_socket.getsockname())
	# while True:
	# 	try:
	# 		tcp_socket.sendall("sss")
	# 	except Exception,e:
	# 		print e



    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", 10000))

    sock.listen(10)

    while True:
    	tcp_socket , addr = sock.accept()
    	while True:
    		tcp_socket.sendall("aaa")
    		import time
    		time.sleep(2)

if __name__ == '__main__':
	#parse_args()
	main()