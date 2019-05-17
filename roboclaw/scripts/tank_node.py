#!/usr/bin/env python
import roslib
import rospy
import math

from std_msgs.msg import Float32
from geometry_msgs.msg import Vector3
from tankMode import tank 

class tank_node:
    def __init__(self):
        self.mctl = Vector3
        self.rover = tank(port='ttyACM0',baud='115200',pwmLimit=102,motorsID=[128,129,130,131,132,133])
        rospy.Subscriber('/Motors/left_vel',Float32,self.left)
        rospy.Subscriber('/Motors/right_vel',Float32,self.right)

        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            #print(self.mctl)
            self.rover.tankDrive(self.mctl)
            r.sleep()

    def left(self,vel):
        self.mctl.x = vel

    def right(self,vel):
        self.mctl.y = vel

if __name__=="__main__":
    rospy.init_node('MotorsAlv')
    #try:
    tank_node()
    #except:
    #    pass
