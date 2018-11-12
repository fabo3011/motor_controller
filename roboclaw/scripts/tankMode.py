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

    def tankDrive(self,rJoy,lJoy):
        if rJoy > 0.2:
            self.goForward('rigth',self.fixPwm(rJoy))
        elif rJoy < 0.2:
            self.goBackward('rigth',self.fixPwm(-rJoy))
        else:
            self.setTo0(rJoy)

        if lJoy > 0.2:
            self.goForward('left',self.fixPwm(lJoy))
        elif lJoy < 0.2:
            self.goBackward('left',self.fixPwm(-lJoy))
        else:
            self.setTo0(lJoy)
        

    def open(self):
        for i in range(0,2):
            if self._rccm[i].Open():
                print(self._rccm._port)
            else: 
                exit("Error: cannot open port: " + self._port[i])
        
    def createRC(self,port,baud):
        for i in range(0,2):
            self._rccm[i] = Roboclaw('/dev/' + port[i], baud)
    
    def goForward(self,side,pwm):
        if side == 'rigth':
            for i in range(0,2):
                self._rccm[i].ForwardM1(self._msID[0],pwm)
        elif side == 'left':
            for i in range(0,2):
                self._rccm.BackwardM1(self._msID[1],pwm)
    
    def goBackward(self,side,pwm):
        if side == 'rigth':
            for i in range(0,2):
                self._rccm[i].BackwardM1(self._msID[0],pwm)
        elif side == 'left':
            for i in range(0,2):
                self._rccm[i].ForwardM1(self._msID[1],pwm)
        else:
            print("Warnig: command not found.")
    
    def setTo0(self,side):
        if side == 'rigth':
            for i in range(0,2):
                self._rccm[i].ForwardM1(self._msID[0],0)
        if side == 'left':
            for i in range(0,2):
                self._rccm[i].ForwardM1(self._msID[1],0)
    
    def fixPwm(self,percentage):
        return long(round(percentage*self._pwml,2))