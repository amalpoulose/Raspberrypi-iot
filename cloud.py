#! /usr/bin/python 

import os
import i2c
import spi
import sys
import temp
import signal
import time
import RPi.GPIO as GPIO
from pubnub import Pubnub
from twilio.rest import Client

channel1="Txt-data"
channel2="Rcv-data"
BULB = 23
TAP=24
FAN = 16
MOTOR =20
client=Client("AC66a94e35bf41165d8d12888f5f59345a","e58e238a3cb43758095af57b0be63edb")

def init():
	GPIO.setmode (GPIO.BCM)
	GPIO.setwarnings(False)

	GPIO.setup(BULB,GPIO.OUT) #setting up bulb pin
	GPIO.setup(FAN,GPIO.OUT)  #setting up fan pin
	GPIO.setup(TAP,GPIO.OUT)  #setting up Tap pin
	GPIO.setup(MOTOR,GPIO.OUT)#setting up motor pin
        #connecting in active low so turn off 
	GPIO.output(BULB,True) 
	GPIO.output(FAN,True)
	GPIO.output(MOTOR,True)
	GPIO.output(TAP,True)

        #change default action of SIGCHLD
	signal.signal(signal.SIGCHLD,handler1)

	pubnub = Pubnub(publish_key='pub-c-08e906fb-45bf-4180-94f1-2e054d86def3', subscribe_key='sub-c-a58a3736-f4fc-11e7-9869-a6bd95f83dd1')
	#initialize adc
	spi.adc_setup()
	return pubnub

def callback(m): #publishing status
   print(m)

def __callback__(m, channel):    #subscribing status
	if 'bulb' in m :
		if m['bulb'] == 1:
			    GPIO.output(BULB,False)
			    print "bulb on"
		else:
			    GPIO.output(BULB,True)
			    print "bulb off"
	if 'fan' in m:
		if m['fan'] == 1:
			    GPIO.output(FAN,False)
			    print "fan on"
		else:
			    GPIO.output(FAN,True)
			    print "fan off"
	if 'motor' in m:
		if m['motor'] == 1:
			    GPIO.output(MOTOR,False)
			    print "motor on"
		else:
			    GPIO.output(MOTOR,True)
			    print "motor off"
		

def __error__(m):  #error while subscribing
	print(m)

def handler1(signum,frame): #Action performed for SIGCHLD signal
     try:
	os.wait()
	print "child exited"
     except OSError:
	pass


def main():

  pubnub=init()
  pubnub.subscribe(channels=channel2, callback=__callback__, error=__error__)

  bulb_flg=0
  tap_flg=0
  fan_flg=0

  while(1):
      #reading LDR value
	LDR=spi.adc_read(0)
      #reading IR value 
	IR=spi.adc_read(1)
      #reading RTC value
	t=i2c.i2c_time()
      #reading temperature value
	temperature=temp.read_temp()

        os.system("clear")

      #printing values
	print "LDR : ",LDR
	print "IR : ",IR
	print "Time : ",t
	print "Temperature : ",temperature," c"

      # Automation using LDR to turn on and turn off light
	if LDR>3600 and bulb_flg==0:
	 cid=os.fork() 
	 if cid==0:
	   time.sleep(3)
	   LDR=spi.adc_read(0)
	   if LDR>3600: 
		data = {
        		'BULB':'ON'
			}	
		pubnub.publish(channel1, data, callback=callback, error=callback)
	        GPIO.output(BULB,False)
		message=client.messages.create(
					to="+918281985856",
					from_="+14152379832",
					body="Light is turning on at "+t)
		print message.sid
	   sys.exit(0)	
	 bulb_flg=1
	elif LDR<=3600 and bulb_flg==1:
	        GPIO.output(BULB,True)
		bulb_flg=0


      # Automation using IR to turn on and off Tap
	if IR<4000 and tap_flg==0:
	    cid=os.fork()
	    if cid==0:
	        GPIO.output(TAP,False)
		time.sleep(3)
	        GPIO.output(TAP,True)
	        sys.exit(0)

      # Automation using DS18b0 to turn on and turn off light
	if temperature>30.0 and fan_flg==0:
	 cid=os.fork()
	 if cid==0:
	   time.sleep(3)
	   temperature=temp.read_temp()
	   if temperature>30.0: 
		data = {
        		'FAN':'ON'
			}	
		pubnub.publish(channel1, data, callback=callback, error=callback)
	        GPIO.output(FAN,False)
		message=client.messages.create(
					to="+918281985856",
					from_="+14152379832",
					body="AC is turning on at "+t)
		print message.sid
	   sys.exit(0)	
	 fan_flg=1
	elif temperature<=30.0 and fan_flg==1:
	        GPIO.output(FAN,True)


        time.sleep(2)

if __name__ == "__main__":
	main()
