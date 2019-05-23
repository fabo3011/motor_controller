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
        self.setTo0Treshold = 0.05
        self.prevPWM = [0,0,0,0,0,0]
        self.serialDelay = 0.1

    def tankDrive(self,joy):
        
        if joy.y > self.setTo0Treshold:
            #print("call forward R")
            self.goForward('right',self.fixPwm(joy.y))
        elif joy.y < -self.setTo0Treshold:
            #print("call backward R")
            self.goBackward('right',self.fixPwm(-joy.y))
        else:
            #print("call setTo0 R")
            self.setTo0('right')

        if joy.x > self.setTo0Treshold:
            #print("call forward L")
            self.goForward('left',self.fixPwm(joy.x))
        elif joy.x < -self.setTo0Treshold:
            #print("call backward L")
            self.goBackward('left',self.fixPwm(-joy.x))
        else:
            #print("call setTo0 L")
            self.setTo0('left')
       # speed = self.ReadSpeed(self.msID)
        return 0
        
    def open(self):
        for i in range(1):
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
    
    def PWMChanged(self, motor, pwm):
        if pwm != self.prevPWM[motor]:
            self.prevPWM[motor] = pwm
            return True
        return False

    def goForward(self,side,pwm):
        for i in range(3):
            if side == 'right' and self.PWMChanged(i, pwm):
                print("goForward R: "+str(self.msID[i])+" "+str(pwm))
                time.sleep(self.serialDelay)
                self.rccm.ForwardM1(self.msID[i],pwm)
                print("done")
            elif side == 'left' and self.PWMChanged(i+3, pwm):
                print("goForward R: "+str(self.msID[i+3])+" "+str(pwm))
                time.sleep(self.serialDelay)
                self.rccm.BackwardM1(self.msID[i+3],pwm)
                print("done") 

    def goBackward(self,side,pwm):
        for i in range(3):
            if side == 'right' and self.PWMChanged(i, -pwm):
                print("goBackward R: "+str(self.msID[i])+" "+str(pwm))
                time.sleep(self.serialDelay)
                self.rccm.BackwardM1(self.msID[i],pwm)
                print("done")
            elif side == 'left' and self.PWMChanged(i+3, -pwm):
                print("goBackward L: "+str(self.msID[i+3])+" "+str(pwm))
                time.sleep(self.serialDelay)
                self.rccm.ForwardM1(self.msID[i+3],pwm)
                print("done")
    
    def setTo0(self,side):
        for i in range(3):
            if side == 'right' and self.PWMChanged(i, 0):
                print("setTo0 R: "+str(self.msID[i])+" 0")
                time.sleep(self.serialDelay)
                self.rccm.ForwardM1(self.msID[i],0)
                print 'Done'
            elif side == 'left' and self.PWMChanged(i+3, 0):
                print("setTo0 L: "+str(self.msID[i+3])+" 0")
                time.sleep(self.serialDelay)
                self.rccm.ForwardM1(self.msID[i+3],0)
                print 'Done'

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
