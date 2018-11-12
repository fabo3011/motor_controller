#!/usr/bin/env python
import roslib
import rospy
import math

from geometry_msgs.msg import Joy
from geometry_msgs.msg import Vector3
from tankMode import tank 

class tank_node:
    def __init__(self):
        rospy.on_shutdown(self.cleanup)
        self._mctl = Vector3()
        self._actl = Vector3()
        self._rover = tank(port=['ttyACM0','ttyACM1','ttyACM2'],baud='115200',pwmLimit=102,motorsID=[128,129])

        rospy.Subscriber('joy',Joy,self.sideCB)
        rospy.Subscriber('positomate!',Vector3,self.armCB)

        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            if self._mctl == 0:
                self._rover.tankDrive(self._ctls)
            else:
                self._rover.armDrive(self._actl)
            r.sleep()
    
    def sideCB(self,joy):
        self._mctl.x = joy.axes[1]
        self._mctl.y = joy.axes[4]
        self._mctl.z = joy.button[2]
    
    def armCB(self,cam):
        self._actl.x = cam.x
        self._actl.y = cam.y
        self._actl.z = cam.z

    def cleanup(self):
        self._rover.setTo0('rigth')
        self._rover.setTo0('left')