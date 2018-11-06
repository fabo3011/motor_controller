#/usr/bin/env python

#Ros libs
import rospy
from sensor_msgs.msg import Joy

#python libs
from sys import exit

#Roboclaw lib
from roboclaw import Roboclaw

#valiables
data = [0,0]

#driver port
port = "ttyACM0"
#baudrate
brte = "115200"
#vel max
vlmx = 6187
#driver addresses
#      [M1  ,M2  ,M3  ,M4  ,M5  ,M6 ]
mtor = [128,129,130,131,132,133]

#set dirver
rc = Roboclaw('/dev/' + port, brte)

#fuctions
def callback(joys):
	global data
    
    
	data[0] = joys.axes[1]
	data[1] = joys.axes[4]
	print("------------------------")
	print(data)
	print("++++++++++++++++++++++++")
	  
#set right motors
    #Foward
	if data[0] > 0.02:
		rc.ForwardM1(mtor[3],long(data[0])*127)
		rc.ForwardM1(mtor[4],long(data[0])*127)
		rc.ForwardM1(mtor[5],long(data[0])*127)
		#rc.SpeedM1(mtor[i],data[0]*vlmx)
    #Backward
	elif data[0] < 0.02:
		rc.BackwardM1(mtor[0],long(abs(data[0]))*127)
		rc.BackwardM1(mtor[4],long(abs(data[0]))*127)
		rc.BackwardM1(mtor[5],long(abs(data[0]))*127)
		#rc.SpeedM1(mtor[i],data[0]*-vlmx)
    #set to 0 
	else:
		rc.ForwardM1(mtor[3],0)
		rc.ForwardM1(mtor[4],0)
		rc.ForwardM1(mtor[5],0)
		#rc.SpeedM1(mtor[i],0)
                
#set left motors
    #Forward
	if data[1] > 0.02:
		rc.ForwardM1(mtor[0],long(data[1])*127)
		rc.ForwardM1(mtor[1],long(data[1])*127)
		rc.ForwardM1(mtor[2],long(data[1])*127)
		#rc.SpeedM1(mtor[i],data[1]*vlmx)
	#Backward
	elif data[1] < 0.02:
		rc.BackwardM1(mtor[0],long(abs(data[1]))*127)
		rc.BackwardM1(mtor[1],long(abs(data[1]))*127)
		rc.BackwardM1(mtor[2],long(abs(data[1]))*127)
		#rc.SpeedM1(mtor[i],data[1]*vlmx)
	#Set to 0
	else:
		rc.ForwardM1(mtor[0],0)
		rc.ForwardM1(mtor[1],0)
		rc.ForwardM1(mtor[2],0)
    	#rc.SpeedM1(mtor[i],0)
	
            
def initnode():
    global rc
    rospy.init_node('motor_test2', anonymous=True)
    rospy.Subscriber('joy',Joy,callback)
    if rc.Open():
        print (rc._port)
    else:
        exit("Error[1]: cannot open prot: " + port)
    rospy.spin()
    
#Main
if __name__=="__main__":
	initnode()
