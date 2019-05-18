#!/usr/bin/env python

import roslib
import rospy

from sensor_msgs.msg import Joy
from std_msgs.msg import Float32
from std_msgs.msg import UInt8

class input_sel:
    def __init__ (self):
        self.joy2rVel = Float32()
        self.joy2lVel = Float32()
        self.aut2rVel = Float32()
        self.aut2lVel = Float32()
        self.left_Vel = Float32()
        self.rightVel = Float32()
	self.modeVel  = UInt8()

        rospy.Subscriber('/Motors/mode',UInt8,self.sideCB)
        rospy.Subscriber('joy',Joy,self.joy2linvel)
        rospy.Subscriber('/BaseController/left_vel',Float32,self.leftCB)
        rospy.Subscriber('/BaseController/right_vel',Float32,self.rightCB)

        lvel_pub = rospy.Publisher('/Motors/left_vel',Float32,queue_size=10)
        rvel_pub = rospy.Publisher('/Motors/right_vel',Float32,queue_size=10)

        rate = rospy.Rate(10)

        while not rospy.is_shutdown():
            rospy.loginfo("left vel: %f   right vel: %f" % (self.left_Vel.data,self.rightVel.data) )
	    selectVelByMode()
            lvel_pub.publish(self.left_Vel)
            rvel_pub.publish(self.rightVel)
            rate.sleep()

    def selectVelByMode(self):
        if   self.modeVel == 1:   #JOY mode

            self.left_Vel.data = self.joy2lVel.data
            self.rightVel.data = self.joy2rVel.data

        elif self.modeVel == 2:   #Autonomous mode

            self.left_Vel.data = self.aut2lVel.data
            self.rightVel.data = self.aut2rVel.data

        elif self.modeVel == 3:   #Stop Rover 

            self.left_Vel.data = 0
            self.rightVel.data = 0

        else:                   #Invalid msg

            rospy.loginfo('Invalid msg, stopping robot')
            self.left_Vel.data = 0
            self.rightVel.data = 0

    def sideCB (self,cmode):
        self.modeVel = cmode.data

    def joy2linvel(self,joy):
        self.joy2rVel.data = joy.axes[1]
        self.joy2lVel.data = joy.axes[3]
    
    def leftCB (self,float32):
        self.aut2lVel.data = float32.data

    def rightCB (self,float32):
        self.aut2rVel.data = float32.data

if __name__ == '__main__':
    rospy.init_node('Mode_selection',anonymous=True)
    input_sel()
