#!/usr/bin/env python

from sys import exit

from roboclaw import Roboclaw

class tank:
    def __init__(self,port,baud,pwmLimit,motorsID):
        self.pord = port
        print("koko")
        self.brte = baud
        self.pwml = pwmLimit
        self.msID = motorsID
        print("skdf")
        self.rccm = self.createRC(port,baud)
        print("caca")
        self.open()

    def tankDrive(self,joy):
        print("dfdf")
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
        print("dfsd")
        self.pich(arm.y)
        print("sdfsdfsdfs")
        self.yaw(arm.z)
        print("ffif")
        self.Forward(arm.x)
        print("fsfdsfdsdf")

        
    def open(self):
        print("caca2")
        for i in range(0,3):
            #print (self.rccm)
            if self.rccm[i].Open():
               print(self.rccm[i]._port)
            else: 
                print("Error: cannot open port: " + self.pord[i])
        
    def createRC(self,port,baud):
        print(port)
        listrc = [None,None,None]
        for i in range(0,3):
            print("kokoko")
            listrc[i] = Roboclaw('/dev/' + port[i], baud)
        return listrc

    def goForward(self,side,pwm):
        if side == 'rigth':
            for i in range(1,2):
                self.rccm[i].ForwardM1(self.msID[0],pwm)
        elif side == 'left':
            for i in range(1,2):
                self.rccm[i].BackwardM1(self.msID[1],pwm)
    
    def Forward(self,x):
        print("uno")
        if x == 1:
            print('fdf')
            self.goForward('right',50)
            self.goForward('left',50)    
        else:
            print('wewew')
            self.setTo0('right')
            self.setTo0('left')    

    def goBackward(self,side,pwm):
        if side == 'rigth':
            for i in range(1,2):
                self.rccm[i].BackwardM1(self.msID[0],pwm)
        elif side == 'left':
            for i in range(1,2):
                self.rccm[i].ForwardM1(self.msID[1],pwm)
        else:
            print("Warnig: command not found.")
    
    def pich(self,id):
        if id == 1:
            self.rccm[0].ForwardM1(self.msID[0],80)
        elif id == -1:
            self.rccm[0].BackwardM1(self.msID[0],80)
        else:
            self.rccm[0].ForwardM1(self.msID[0],0)
    
    def yaw(self,id):
        if id == 1:
            self.rccm[0].ForwardM1(self.msID[1],20)
        elif id == -1:
            self.rccm[0].BackwardM1(self.msID[1],20)
        else:
            self.rccm[0].ForwardM1(self.msID[1],0)

    def setTo0(self,side):
        if side == 'rigth':
            for i in range(1,2):
                self.rccm[i].ForwardM1(self.msID[0],0)
        if side == 'left':
            for i in range(1,2):
                self.rccm[i].ForwardM1(self.msID[1],0)
    
    def fixPwm(self,percentage):
        return long(round(percentage*self.pwml,2))
