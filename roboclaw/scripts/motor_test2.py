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
#         BR        BL         Front
port = ["ttyACM0","ttyACM1","ttyACM2"]
#baudrate
brte = "115200"
#vel max
vlmx = 6187
#driver addresses
#      [M1  ,M2  ,M3  ,M4  ,M5  ,M6 ]
mtor = [128,129]

#pwm limit
pwm = 102

#set dirver
#Back Rigth
rc0 = Roboclaw('/dev/' + port[0], brte)
#Back Left
rc1 = Roboclaw('/dev/' + port[1], brte)
#Front
rc2 = Roboclaw('/dev/' + port[2], brte)
#fuctions
def callback(joys):
	global data
	global pwm

	data[0] = long(round(joys.axes[1]*pwm,0))
	data[1] = long(round(joys.axes[4]*pwm,0))
	print("------------------------")
	print(data)
	print("++++++++++++++++++++++++")
	  
#set left motors
    #Foward
	if data[0] > 0.02:
		rc2.ForwardM1(mtor[0],data[0])
		rc1.ForwardM1(mtor[0],data[0])
		rc1.ForwardM1(mtor[1],data[0])
		#rc.SpeedM1(mtor[i],data[0]*vlmx)
    #Backward
	elif data[0] < 0.02:
		rc2.BackwardM1(mtor[0],-data[0])
		rc1.BackwardM1(mtor[0],-data[0])
		rc1.BackwardM1(mtor[1],-data[0])
		#rc.SpeedM1(mtor[i],data[0]*-vlmx)
    #set to 0 
	else:
		rc2.ForwardM1(mtor[0],0)
		rc1.ForwardM1(mtor[0],0)
		rc1.ForwardM1(mtor[1],0)
		#rc.SpeedM1(mtor[i],0)
                
#set rigth motors
    #Forward
	if data[1] < 0.02:
		rc2.ForwardM1(mtor[1],-data[1])
		rc0.ForwardM1(mtor[1],-data[1])
		rc0.ForwardM1(mtor[0],-data[1])
		#rc.SpeedM1(mtor[i],data[1]*vlmx)
	#Backward
	elif data[1] > 0.02:
		rc2.BackwardM1(mtor[1],data[1])
		rc0.BackwardM1(mtor[1],data[1])
		rc0.BackwardM1(mtor[0],data[1])
		#rc.SpeedM1(mtor[i],data[1]*vlmx)
	#Set to 0
	else:
		rc2.ForwardM1(mtor[1],0)
		rc0.ForwardM1(mtor[1],0)
		rc0.ForwardM1(mtor[0],0)
    	#rc.SpeedM1(mtor[i],0)
	
            
def initnode():
    global rc0
    rospy.init_node('motor_test2', anonymous=True)
    rospy.Subscriber('joy',Joy,callback)
    if rc0.Open() and rc1.Open() and rc2.Open():
        print (rc0._port)
        print ("-------------")
        print (rc1._port)
        print ("==============")
        print (rc2._port)
    else:
        exit("Error[1]: cannot open prot: " + port)
    rospy.spin()
    
#Main
if __name__=="__main__":
	initnode()
