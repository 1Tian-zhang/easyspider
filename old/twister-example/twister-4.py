#coding=utf-8

#变成非阻塞模型

import argparse,socket,select


def parse_cmdline():
	parser = argparse.ArgumentParser("接收端口输出")
	parser.add_argument("-p","--port",default=10000,type=int,nargs="+",choices=[i for i in xrange(1,65536)])
	args = parser.parse_args()
	#注意lambda的括号是括在哪里
	return map(lambda port:("127.0.0.1",int(port)) ,args.port)


def get_poetry(socket_list):
	#防止传进来的参数被改变...如果改变了，到时候传到后面就不好用了
	#所以制作了一个副本
	socket_list = list(socket_list) #make a copy

	#通过一个列表来生成字典，后面的是默认的值，因为同时获取不同的诗歌
	#所以需要一个字典来记录一下　　一个字典就是通过列表按照socket生成的
	poems = dict.fromkeys(socket_list,"")

	#再来一个记录是那个任务
	sock2task = dict([ (s,i+1) for i,s in enumerate(socket_list)])
	
	while socket_list:
		rlist, _ ,_ = select.select(socket_list,[],[])

		for sock in rlist:
			data = ""
			while True:
				try:
					new_data = sock.recv(1024)
				except socket.error,e:
					print e
					break

				if not new_data:
					break
				else:
					data += new_data

			task_num = sock2task[sock]
			if not data:
				#移除成功的socket
				socket_list.remove(sock)
				sock.close()
				print "task %d finished"%(task_num)
			else:
				print "task %d received %d"%(task_num,len(data))
	return poems

def make_conn_sock(address):
	sock = socket.socket()
	sock.connect(address)
	sock.setblocking(0)
	return sock

def main():
	address_list = parse_cmdline()
	socket_list = map(make_conn_sock,address_list)
	poem = get_poetry(socket_list)



if __name__ == '__main__':
	main()


