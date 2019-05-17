#!usr/bin/env python

import roslib
import rospy

from sensor_msgs.msg import Joy
from std_msgs.msg import Float32
from std_msgs.msg import Char

class input_sel:
    def __init__ (self):
        self.joy2rVel = Float32()
        self.joy2lVel = Float32()
        self.aut2rVel = Float32()
        self.aut2lVel = Float32()
        self.left_Vel = Float32()
        self.rightVel = Float32()

        rospy.Subscriber('/Motors/mode',Char,self.sideCB)
        rospy.Subscriber('joy',Joy,self.joy2linvel)
        rospy.Subscriber('/BaseController/left_vel',Float32,self.leftCB)
        rospy.Subscriber('/BaseController/right_vel',Float32,self.rightCB)

        lvel_pub = rospy.Publisher('/Motors/left_vel',Float32,queue_size=10)
        rvel_pub = rospy.Publisher('/Motors/right_vel',Float32,queue_size=10)

        rate = rospy.Rate(10)

        while not rospy.is_shutdown():
            rospy.loginfo("left vel: %f   right vel: %f" % self.left_Vel %self.rightVel )
            lvel_pub.publish(self.left_Vel)
            rvel_pub.publish(self.rightVel)
            rate.sleep()

    def sideCB (self,cmode):
        if cmode == 'j':
            self.left_Vel = self.joy2lVel
            self.rightVel = self.joy2rVel
        elif cmode == 'i':
            self.left_Vel = self.aut2lVel
            self.rightVel = self.aut2rVel
        elif cmode == 's':
            self.left_Vel = 0
            self.rightVel = 0
        else:
            rospy.loginfo('MAAAMEEEEES, ponte vergas y pon < j > para manual o < i > para autonomia o interfaz')
            self.left_Vel = 0
            self.rightVel = 0

    def joy2linvel(self,joy):
        self.joy2rvel = joy[1]
        self.joy2lVel = joy[4]
    
    def leftCB (self,float32):
        self.aut2lVel = float32

    def rightCB (self,float32):
        self.aut2rVel = float32

if __name__ == '__main__':
    rospy.init_node('Mode_selection',anonymous=True)
    input_sel()