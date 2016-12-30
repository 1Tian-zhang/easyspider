#coding=utf-8

import socket
import fcntl
import struct

#interface_name = "wlp3s0"


#if_name 网卡的名字，默认eth0
def get_ip(if_name="eth0"):
	s = socket.socket()
	flag , ip = [True],None
	try:
		ip = socket.inet_ntoa(
			fcntl.ioctl(
				s.fileno(),
				0x8915, #SIOCGIFADDR
				struct.pack("256s",if_name[:15])
				)[20:24]
			)
	except IOError,e:
		reason = "interface name is not avaliable"
		flag[0] = False
		flag.append("False,%s"%reason)
	except Exception,e:
		reason = e
		flag[0] = False
		flag.append("False,%s"%reason)
	return flag,ip


def main():
	#print get_ip("wlp3s0aa")

	flag , ip = get_ip(interface_name)
	#if not flag[:4]:
	#	print flag
	#else:
	#	print ip
	if not flag[0]:
		print flag[1]
	else:
		print ip

if __name__ == '__main__':
	main()