#coding=utf-8
import socket
import fcntl
import struct


def get_ip(ifname):  
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    return socket.inet_ntoa(fcntl.ioctl(  
        s.fileno(),  
        0x8915, # SIOCGIFADDR  
        struct.pack('256s', ifname[:15])  
    )[20:24])  


# import socket
# localIP = socket.gethostbyname(socket.gethostname())#得到本地ip
# print "local ip:%s "%localIP
 
# ipList = socket.gethostbyname_ex(socket.gethostname())
# for i in ipList:
#     if i != localIP:
#        print "external IP:%s"%i

print get_ip("wlp3s0")