#coding=utf-8

#import useragent

#from middlewares import useragent

#from items.items import ExampleItem

print "hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"


import signal

# def myHandler(signum,frame):
# 	print "i received ",signum

# signal.signal(signal.SIGTSTP,myHandler)

# signal.pause()

# print("end of signal demo")



signal_names = {}
for signame in dir(signal):
    if signame.startswith("SIG"):
        signum = getattr(signal, signame)
        if isinstance(signum, int):
            signal_names[signum] = signame

print signal_names

while True:
	print "Hello,i am test"