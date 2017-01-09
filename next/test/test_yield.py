#coding=utf-8


# 1 1 2 3 5 8

def fab(n):
	if n==1 or n==2:
		return 1
	i=2
	a,b,c= 1,1,0
	while i<n:
		#c = a+b
		#a = b
		#b = c
		a,b = b,a+b
		i+=1
		#print c
	return b


print fab(6)
