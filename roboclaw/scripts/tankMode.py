#!/usr/bin/env python

from sys import exit

from roboclaw import Roboclaw

class tank:
    def __init__(self,port,baud,pwmLimit,motorsID):
        self._port = port
        self._brte = baud
        self._pwml = pwmLimit
        self._msID = motorsID
        self._rccm = self._createRC(self._port,self._brte)
        self._open()

    def tankDrive(self,joy):
        if joy.y > 0.2:
            self.goForward('rigth',self.fixPwm(joy.y))
        elif joy.y < 0.2:
            self.goBackward('rigth',self.fixPwm(-joy.y))
        else:
            self.setTo0('rigth')

        if joy.x > 0.2:
            self.goForward('left',self.fixPwm(joy.x))
        elif joy.x < 0.2:
            self.goBackward('left',self.fixPwm(-joy.x))
        else:
            self.setTo0('left')
    def armDrive(self,arm):
        self.pich(arm.y)
        self.yaw(arm.z)
        self.Froward(arm.x)

        
    def open(self):
        for i in range(1,2):
            if self._rccm[i].Open():
                print(self._rccm._port)
            else: 
                exit("Error: cannot open port: " + self._port[i])
        
    def createRC(self,port,baud):
        for i in range(1,2):
            self._rccm[i] = Roboclaw('/dev/' + port[i], baud)
    
    def goForward(self,side,pwm):
        if side == 'rigth':
            for i in range(1,2):
                self._rccm[i].ForwardM1(self._msID[0],pwm)
        elif side == 'left':
            for i in range(1,2):
                self._rccm.BackwardM1(self._msID[1],pwm)
    
    def Forward(self,x):
        if x == 1:
            self.goForward('right',50)
            self.goForward('left',50)        

    def goBackward(self,side,pwm):
        if side == 'rigth':
            for i in range(1,2):
                self._rccm[i].BackwardM1(self._msID[0],pwm)
        elif side == 'left':
            for i in range(1,2):
                self._rccm[i].ForwardM1(self._msID[1],pwm)
        else:
            print("Warnig: command not found.")
    
    def pich(self,id):
        if id == 1:
            self._rccm[0].ForwardM1(self._msID[0],50)
        elif id == -1:
            self._rccm[0].BackwardM1(self._msID[0],50)
        else:
            self._rccm[0].ForwardM1(self._msID[0],0)
    
    def yaw(self,id):
        if id == 1:
            self._rccm[0].ForwardM1(self._msID[1],50)
        elif id == -1:
            self._rccm[0].BackwardM1(self._msID[1],50)
        else:
            self._rccm[0].ForwardM1(self._msID[1],0)

    def setTo0(self,side):
        if side == 'rigth':
            for i in range(1,2):
                self._rccm[i].ForwardM1(self._msID[0],0)
        if side == 'left':
            for i in range(1,2):
                self._rccm[i].ForwardM1(self._msID[1],0)
    
    def fixPwm(self,percentage):
        return long(round(percentage*self._pwml,2))