#!/usr/bin/env python

from sys import exit

from roboclaw import Roboclaw

class tank:
    def __init__(self,port,baud,pwmLimit,motorsID):
        self.pord = port
        self.brte = baud
        self.pwml = pwmLimit
        self.msID = motorsID
        self.rccm = self.createRC(port,baud)
        self.open()

    def tankDrive(self,joy):
        if joy.y > 0.2:
            self.goForward('rigth',self.fixPwm(joy.y))
        elif joy.y < -0.2:
            self.goBackward('rigth',self.fixPwm(-joy.y))
        else:
            self.setTo0('rigth')

        if joy.x > 0.2:
            self.goForward('left',self.fixPwm(joy.x))
        elif joy.x < -0.2:
            self.goBackward('left',self.fixPwm(-joy.x))
        else:
            self.setTo0('left')
        
    def open(self):
        for i in range(0,3):
            #print (self.rccm)
            if self.rccm[i].Open():
               print(self.rccm[i]._port)
            else: 
                exit("Error: cannot open port: " + self.pord[i])

    def createRC(self,port,baud):
        print(port)
        listrc = [None,None,None]
        for i in range(3):
            listrc[i] = Roboclaw('/dev/' + port[i], baud)
        return listrc

    def goForward(self,side,pwm):
        if side == 'rigth':
            for i in range(3):
                self.rccm[i].ForwardM1(self.msID[0],pwm)
        elif side == 'left':
            for i in range(3):
                self.rccm[i].BackwardM1(self.msID[1],pwm)  

    def goBackward(self,side,pwm):
        if side == 'rigth':
            for i in range(3):
                self.rccm[i].BackwardM1(self.msID[0],pwm)
        elif side == 'left':
            for i in range(3):
                self.rccm[i].ForwardM1(self.msID[1],pwm)
        else:
            print("Warnig: command not found.")
    
    def setTo0(self,side):
        if side == 'rigth':
            for i in range(3):
                self.rccm[i].ForwardM1(self.msID[0],0)
        if side == 'left':
            for i in range(3):
                self.rccm[i].ForwardM1(self.msID[1],0)

    def fixPwm(self,percentage):
        return long(round(percentage*self.pwml,2))
