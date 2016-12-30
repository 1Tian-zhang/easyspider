#coding=utf-8
#接收前面那一个的诗歌

import argparse,socket

def parse_cmdlines():
	#必须先申明能接受什么参数，不然的话，如果提供了一个没有申明的参数，就会error: unrecognized arguments: -P 123
	#-h 和　--help 都可以
	parser = argparse.ArgumentParser(description="用来接收第一次的诗歌服务")

	#可以接受　"123"　这种只要能转化成int就行
	
	#但是不可以　-P 大p不行
	
	#-p 123 / -p123 / -p=123 这三种都可以
	
	#除了-p　，后面还加了一个--port　，一个是简写形式，一个是　--两个横杆长参数
	#上面说了，对于简写形式可以-p123，但是对于长参数，就不可以 --port123 了，只能空格或者等于。否则就会报错:error: unrecognized arguments: --port123

	#加个列表，然后指定　choices 表示只能在这几个列表里面选择。比如只能指定１-10的端口，输入１００的话就会报错 error: argument -p/--port: invalid choice: 100 (choose from 1, 2, 3, 4, 5, 6, 7, 8, 9)

	#加个default 的话，表示是默认参数...注意这个默认参数很有趣...允许选择的只有１－９但是默认参数允许默认到１００００，１Ｗ

	#metavar 是在Usage中说明的参数名称. 没有提供的话，参数默认就是参数的名称，如果有写，那么在help中看到的效果是这个样子的

	# $ python twister-2.py -h
	# usage: twister-2.py [-h] [-p 这个参数是端口参数]

	# 用来接收第一次的诗歌服务

	# optional arguments:
	#   -h, --help            show this help message and exit
	#   -p 这个参数是端口参数, --port 这个参数是端口参数
	#                         指定接收消息的端口

	#上面的，很漂亮~

	#dest: 解析后的参数名称，默认情况下，对可选参数，选择最长的名称，中划线转变为下划线。
	#比如，如果没有指定　dest 的情况下，而 --port 又有，那么解析到参数就是　Namespace(port=5)
	#而加了这个dest...那么解析到的就是Namespace(myport=5)
	#而如果没加，而--port　有没有的话...就是 Namespace(p=5)

	#required　表示这个参数是否是可选的，因为已经设定了default 所以有没有这个required　都没有关系
	#但是required可以覆盖default，如果required是True的话，即使设置了default,也会报错
	#error: argument -p/--port is required
	#所以如果有default的话，基本都可以不用写

	#nargs 表示参数的个数，常用在这种情况...同时监听好几个端口　-p 1 2 3 4 5
	#监听这么多个端口，那么就会有这么多个参数。如果不写nargs的话，就只能接受一个参数，多了就会出错
	#error: unrecognized arguments: 2 3 4 5 　除了１，后面的参数都不认...
	#　nargs　可以是具体的数字，也可以是正则那样， * 是０或者多个，+　是一个和多个　？　也能算
	#但是如果是０个的话，那么就把defalut 覆盖掉了...所以还是写　＋
	parser.add_argument("-p","--port",type=int,help="指定接收消息的端口",choices=[i for i in xrange(1,10)],default=10000,metavar="这个参数是端口参数",dest="myport",required=False,nargs="+") 

	#还有一个很有意思的事情...我如果就这样什么都不添加的话，是可以直接跟参数不要名字的
	#python twister-2.py 123 直接变成　Namespace(myport=10000, test='123')
	#不需要加上一个横杆或者两个横杆的参数 如果有多个这样什么都不加的话，那么就是根据参数的顺序来的
	#而且必须要给....估计　rm xx -rf 这样子的　xx　就是必须要给定，但是没有写的参数
	#parser.add_argument("test")
	#parser.add_argument("test2")
	args = parser.parse_args()

	#下面这个新版已经没有这个方法了，要访问的话，只有通过点属性去访问
	#options,args = parser.parse_args()
	#print options,args
	print args.myport
	print args
	#return options,args
	return 1,2


def main():
	options , args = parse_cmdlines()


if __name__ == '__main__':
	main()