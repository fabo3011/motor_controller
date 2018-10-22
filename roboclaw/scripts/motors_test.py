#!/usr/bin/env python

#ROS libraries
import rospy
from sensor_msgs.msg import Joy

#python libraries
from sys import exit

#Roboclaw library
from roboclaw import Roboclaw

#global valriables
pwm = 0
lpwm = 0
#driver prot
dport = "ttyACM0"
#Baud rate
brate = "115200"
#driver address
address = 0x80
#driver object
rc = Roboclaw('/dev/' + dport, brate)

#functions
def callback(data):
	global pwm
	global lpwm
	lpwm = pwm
	pwm = data.axes[1]

#def setpwm():
	global pwm
	global lpwm
	global address
	rospy.loginfo("test 1")
#	while 1:
	if abs(lpwm-pwm) > .002:
		rospy.loginfo("test 2")
		lpwm = pwm
		rospy.loginfo("test 3")
		if pwm > 0.02 :
			rospy.loginfo(pwm)
			rc.ForwardM1(address,(long(pwm*127)))
		elif pwm < 0.02:
			rospy.loginfo(pwm)
			rc.BackwardM1(address,(long(pwm*-127)))
		else:
			rc.FowardM1(address,0)
	else:
		rospy.loginfo("No change")
#		rospy.spin()

def initnode():
	global rc
	rospy.init_node('motor_test',anonymous=True)
	rospy.Subscriber('joy',Joy, callback)
	if rc.Open():
		print (rc._port)
	else:
		exit("Error at try open port " + dport)
	rospy.spin()
#Main
if __name__=='__main__':
	initnode()
	rospy.loginfo("init setpwm")
#	setpwm()
