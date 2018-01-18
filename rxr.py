
#! /usr/bin/python2.7
from pubnub import Pubnub

pub =Pubnub(publish_key='pub-c-08e906fb-45bf-4180-94f1-2e054d86def3', 
				subscribe_key='sub-c-a58a3736-f4fc-11e7-9869-a6bd95f83dd1')
channel="my_channel"

def __callback(m,channel):
	print m
	print "string received is ", m["data"]

def __error(m):        
	print m#or do something

def main():
	pub.subscribe(channels=channel,callback=__callback,error=__error)

if __name__=="__main__":
	main()
