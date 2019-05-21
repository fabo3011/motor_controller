#!/usr/bin/env python

from sys import exit
import rospy
import os
import time

from roboclaw import Roboclaw

class tank:
    def __init__(self,port,baud,pwmLimit,motorsID):
        self.pord = port
        self.brte = baud
        self.pwml = pwmLimit
        self.msID = motorsID
        self.rccm = self.createRC(port,baud)
        self.open()
        self.resetEnc(motorsID)

    def tankDrive(self,joy):
        
        if joy.y > 0.02:
            print(1)
            self.goForward('right',self.fixPwm(joy.y))
        elif joy.y < -0.02:
            self.goBackward('right',self.fixPwm(-joy.y))
        else:
            self.setTo0('right')

        if joy.x > 0.02:
            self.goForward('left',self.fixPwm(joy.x))
        elif joy.x < -0.02:
            self.goBackward('left',self.fixPwm(-joy.x))
        else:
            self.setTo0('left')
       # speed = self.ReadSpeed(self.msID)
        return 0
        
    def open(self):
        for i in range(10):
            rospy.loginfo("waiting port: %s. %i sec." %(self.pord,10-i))
            time.sleep(1)
        else:
            rospy.loginfo("open port: %s" %self.pord)
            os.system("sudo chmod 777 /dev/" + self.pord)
            rospy.loginfo("port: %s opened" %self.pord)
        if self.rccm.Open():
            print(self.rccm._port)
        else: 
            exit("Error: cannot open port: " + self.pord)

    def createRC(self,port,baud):
        listrc = Roboclaw('/dev/' + port, baud)
        return listrc

    def goForward(self,side,pwm):
        for i in range(3):
            if side == 'right':
                print(2)
                self.rccm.ForwardM1(self.msID[i],pwm)
                print(3)
                time.sleep(0.050)
            elif side == 'left':
                self.rccm.BackwardM1(self.msID[i+3],pwm)
                time.sleep(0.050)
            else:
                print("Warnig: command not found.")  

    def goBackward(self,side,pwm):
        for i in range(3):
            if side == 'right':
                self.rccm.BackwardM1(self.msID[i],pwm)
            elif side == 'left':
                self.rccm.ForwardM1(self.msID[i+3],pwm)
            else:
                print("Warnig: command not found.")
    
    def setTo0(self,side):
        
        for i in range(3):
            if side == 'right':
                self.rccm.ForwardM1(self.msID[i],0)
            elif side == 'left':
                self.rccm.ForwardM1(self.msID[i+3],0)

    def fixPwm(self,percentage):
        return long(round(percentage*self.pwml,2))

    def resetEnc(self,idS):
        for i in range(6):
            self.rccm.ResetEncoders(idS[i])
    
    def ReadSpeed(self,idS):
        speed = []
        for i in range (6):
            if i%2 == 0:
                speed[i*2] = idS[i]
            else:
                speed[i*2+1] = self.rccm.ReadSpeedM1(idS[i])
        return speed