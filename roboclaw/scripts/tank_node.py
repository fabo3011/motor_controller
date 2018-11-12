#!/usr/bin/env python
import roslib
import rospy
import math

from sensor_msgs.msg import Joy
from geometry_msgs.msg import Vector3
from tankMode import tank 

print ("lolo")

class tank_node:
    def __init__(self):
        print("kokok")
        self.mctl = Vector3()
        self.actl = Vector3()
        print (self.mctl)
        self.rover = tank(port=['ttyACM0','ttyACM1','ttyACM2'],baud='115200',pwmLimit=102,motorsID=[128,129])
        print("popo")
        rospy.Subscriber('joy',Joy,self.sideCB)
        rospy.Subscriber('posiTomate',Vector3,self.armCB)

        r = rospy.Rate(10)
        print("fasdkf")
        while not rospy.is_shutdown():
            print(self.actl)
            if self.mctl == 1:
                print("fsd")
                self.rover.tankDrive(self.mctl)
            else:
                print("sfd")
                self.rover.armDrive(self.actl)
            r.sleep()
    
    def sideCB(self,joy):
        self.mctl.x = joy.axes[1]
        self.mctl.y = joy.axes[4]
        self.mctl.z = joy.button[1]
    
    def armCB(self,cam):
        self.actl.x = cam.x
        self.actl.z = cam.y
        self.actl.y = cam.z

if __name__=="__main__":
    print("hola")
    rospy.init_node('rover')
    try:

        tank_node()
    except:
        pass
