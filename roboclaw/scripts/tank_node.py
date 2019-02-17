#!/usr/bin/env python
import roslib
import rospy
import math

from sensor_msgs.msg import Joy
from geometry_msgs.msg import Vector3
from tankMode import tank 

class tank_node:
    def __init__(self):
        self.mctl = Vector3()
        self.actl = Vector3()
        self.rover = tank(port=['ttyACM0','ttyACM1','ttyACM2'],baud='115200',pwmLimit=102,motorsID=[128,129])
        rospy.Subscriber('joy',Joy,self.sideCB)

        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            print(self.actl)
            self.rover.tankDrive(self.mctl)
            r.sleep()
    
    def sideCB(self,joy):
        self.mctl.x = joy.axes[1]
        self.mctl.y = joy.axes[4]

if __name__=="__main__":
    rospy.init_node('rover')
    try:

        tank_node()
    except:
        pass
