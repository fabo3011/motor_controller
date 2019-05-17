#!/usr/bin/env python

from sys import exit

from roboclaw import Roboclaw

class rover:
    def __init__(self,port,baud,pwmLimit,motorsID):
        self.pord = port
        self.brte = baud
        self.pwml = pwmLimit
        self.msID = motorsID
        self.rccm = self.createRC(port,baud)
        self.open()

    '''Functions for the rover movement.
       The folowing fuctions are for 6 wheels'''
    
    #Tank Drive uses 2 joysticks one for the left  side
    #and the other for the rigth side. Uses PWM to move
    #the motors. No Encoders needed.
    def tankDrive(self,joy):
        if joy.y > 0.02:
            self.goForward('rigth',self.fixPwm(joy.y))
        elif joy.y < -0.02:
            self.goBackward('rigth',self.fixPwm(-joy.y))
        else:
            self.setTo0('rigth')

        if joy.x > 0.02:
            self.goForward('left',self.fixPwm(joy.x))
        elif joy.x < -0.02:
            self.goBackward('left',self.fixPwm(-joy.x))
        else:
            self.setTo0('left')

    #This Function moves the rover, tank mode, uses the
    #Encoders tho. 
    #Testing asf;dkljfjlkasd;lfkjafio wish luck and...
    #May the Foce be whit us.
    def tankVel(self,joy):
        self.FastnFurius('rigth',joy.y)
        self.FastnFurius('left',joy.x)
        return self.Speed()
    

    '''Emo Functions, cuz' we need it but are diferent kind. '''
    #Take the Roboclaw's ForwardM1 and use the PWM 
    #and side to move the 3 side motors Pruuu  
    def goForward(self,side,pwm):
        if side == 'rigth':
            for i in range(3):
                self.rccm[i].ForwardM1(self.msID[0],pwm)
        elif side == 'left':
            for i in range(3):
                self.rccm[i].BackwardM1(self.msID[1],pwm)  

    #Same as above but Backward :3 
    def goBackward(self,side,pwm):
        if side == 'rigth':
            for i in range(3):
                self.rccm[i].BackwardM1(self.msID[0],pwm)
        elif side == 'left':
            for i in range(3):
                self.rccm[i].ForwardM1(self.msID[1],pwm)
        else:
            print("Warnig: command not found.")
    
    #Stop the motors... Only PWM :3
    def setTo0(self,side):
        if side == 'rigth':
            for i in range(3):
                self.rccm[i].ForwardM1(self.msID[0],0)
        if side == 'left':
            for i in range(3):
                self.rccm[i].ForwardM1(self.msID[1],0)

    #Retrun the Speed. Just for know. 
    def Speed(self):
        brum = [0,0,0,0,0,0]
        for i in range(3):
                brum[i] = self.rccm[i].ReadSpeedM1(self.msID[0])
                brum[i+3] = self.rccm[i].ReadSpeedM1(self.msID[1])
        return brum 
    
    #Set the Speed we need to all motors :3
    def FastnFurius(self,side,percentage):
        if side == 'rigth':
            for i in range(3):
                self.rccm[i].SpeedM1(self.msID[1],percentage)
        elif side == 'left':
            for i in range(3):
                self.rccm[i].SpeedM1(self.msID[1],percentage)
        else:
            return 'No command found. Speed Error'



    '''Roboclaw Functions
       The folowing fuctions are for the 
       use the Roboclaw's Controller
       better than pololu XD'''

    #Starts the USB Serial port for the 3 Masters.
    # Shoud be one, thest will come whit ESTA OOOHHH    
    def open(self):
        for i in range(0,3):
            #print (self.rccm)
            if self.rccm[i].Open():
               print(self.rccm[i]._port)
            else: 
                exit("Error: cannot open port: " + self.pord[i])

    #Create the 3 Roboclaw objects
    def createRC(self,port,baud):
        print(port)
        listrc = [None,None,None]
        for i in range(3):
            listrc[i] = Roboclaw('/dev/' + port[i], baud)
        return listrc

    '''Extra functions'''

    #Convert the float joy msgs to Long like this OOhh
    def fixPwm(self,percentage):
        return long(round(percentage*self.pwml,2))
