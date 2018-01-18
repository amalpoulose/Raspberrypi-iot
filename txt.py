#! /usr/bin/python2.7
import sys
from pubnub import Pubnub

pub =Pubnub(publish_key='pub-c-08e906fb-45bf-4180-94f1-2e054d86def3', 
				subscribe_key='sub-c-a58a3736-f4fc-11e7-9869-a6bd95f83dd1')
channel="my_channel"

def callback(m):
	print m

def main():
	if len(sys.argv)!=2:
		print "Usage : ./txt string"
		sys.exit(-1)
	data={"data":sys.argv[1]}
	pub.publish(channel,data,callback=callback,error=callback)
if __name__=="__main__":
	main()
