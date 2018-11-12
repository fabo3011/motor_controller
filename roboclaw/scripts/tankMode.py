#!/usr/bin/env python

from sys import exit

from roboclaw import Roboclaw

class tank:
    def __init__(self,port,baud,pwmLimit,motorsID):
        self._port = port
        self._brte = baud
        self._pwml = pwmLimit
        self._msID = motorsID
        self._rccm = self._createRCO(self._port,self._brte)
        self._open()

    def open():
        for i in range(0,2):
            if self._
    
    def createRCO(self):
        for i in range(0,2):
            self._rccm[i] = Roboc('/dev/' + port,baud)
