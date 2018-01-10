#! /usr/bin/python -tt
import RPi.GPIO as gpio
import time
import os
import i2c
mosi=17
miso=18
cs =27
scl=22

def adc_setup():
	gpio.setmode(gpio.BCM)
        gpio.setwarnings(False) 
	gpio.setup(mosi,gpio.OUT)
	gpio.setup(miso,gpio.IN)
	gpio.setup(cs,gpio.OUT)
	gpio.setup(scl,gpio.OUT)
	

def adc_read(channel):
	
	# chip select 0
	gpio.output(cs,False)

	# start bit
	gpio.output(scl,False)
	gpio.output(mosi,True)
	gpio.output(scl,True)
	
	# single/diff bit
	gpio.output(scl,False)
	gpio.output(mosi,True)
	gpio.output(scl,True)
	
	# d2 bit don"t care
	gpio.output(scl,False)
	gpio.output(mosi,True)
	gpio.output(scl,True)
	
	# d1 bit
	gpio.output(scl,False)
	gpio.output(mosi,channel>>1)
	gpio.output(scl,True)
	
	# d2 bit
	gpio.output(scl,False)
	gpio.output(mosi,channel&1)
	gpio.output(scl,True)
	
	# Tsample bit
	gpio.output(scl,False)
	gpio.output(mosi,True)
	gpio.output(scl,True)
	
	# Null bit
	gpio.output(scl,False)
	gpio.output(mosi,True)
	gpio.output(scl,True)
	
	data=0
	for i in range(11,-1,-1):
		gpio.output(scl,False)
		if gpio.input(miso) :
			data |= (1<<i)
		gpio.output(scl,True)
	gpio.output(cs,True)
	return data
		
def main():
	adc_setup()
	while(1):
		os.system("clear")
		data=adc_read(0)
		data1=adc_read(1)
		print "channel : ", data,"   channel2 : ",data1,"  ",i2c.i2c_time() 
		time.sleep(1)

if __name__=="__main__":
		main()
