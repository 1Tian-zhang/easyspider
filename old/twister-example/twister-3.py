#coding=utf-8

#非阻塞获取socket端口/服务器发送的值
#这个一定要等前面一个　for循环执行完后，再来执行下面一个...
#就算把for里面换成　yield　反而却没有作用...什么事都没发生

import argparse,socket


def parse_cmdline():
	parser = argparse.ArgumentParser("接收端口输出")
	parser.add_argument("-p","--port",default=10000,type=int,nargs="+",choices=[i for i in xrange(1,65536)])
	args = parser.parse_args()
	#注意lambda的括号是括在哪里
	return map(lambda port:("127.0.0.1",int(port)) ,args.port)


def get_poetry(address):
	sock = socket.socket()
	print address
	sock.connect(address)
	poem = ""
	while True:
		data = sock.recv(1024)
		if not data:
			sock.close()
			break
		poem+=data
		print "%s reveive %d"%(address,len(poem))
	return poem

def main():
	address_list = parse_cmdline()
	for address in address_list:
		poem = get_poetry(address)
		print poem


if __name__ == '__main__':
	main()


