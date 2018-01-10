#!/usr/bin/python2.7

def read_temp():
	f=file("/sys/bus/w1/devices/28-031500fc5bff/w1_slave","rU")
	f.seek(0,0)
	s=f.read()
	l=s.split()
	f.close()
	return float(l[-1][2:])/1000
