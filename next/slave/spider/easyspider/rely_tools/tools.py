#coding=utf-8


import time


def get_time():
	return time.strftime("%Y-%m-%d %H:%M:%S")


def main():
	print get_time()

if __name__ == '__main__':
	main()