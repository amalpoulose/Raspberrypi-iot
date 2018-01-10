#!/usr/bin/python2.7

import smbus
import time
import sys
import os
import RPi.GPIO as gpio
def init():
     try:
	bus=smbus.SMBus(1)
	t=time.strptime(time.ctime())
        sec=int(str(t[5]),16)
        m=int(str(t[4]),16)
        hr=int(str(t[3]),16)
	bus.write_byte_data(0x68,0x00,sec)
	bus.write_byte_data(0x68,0x01,m)
	bus.write_byte_data(0x68,0x02,hr)
	return bus
     except IOError:
		print "No RTC Found"
		sys.exit(-1)
def i2c_time():
		bus=init()
		hr=bus.read_byte_data(0x68,0x2)
		m =bus.read_byte_data(0x68,0x1)
		s =bus.read_byte_data(0x68,0x0)
		t=str(hex(hr)[2:])+":"+str(hex(m)[2:])+":"+str(hex(s)[2:])
		return t
def main():
        while(1):
		os.system("clear")
		t=i2c_time()
		print t
		time.sleep(1)
if __name__ == "__main__":
	main()

