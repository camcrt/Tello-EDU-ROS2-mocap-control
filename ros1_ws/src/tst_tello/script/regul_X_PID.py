#!/usr/bin/env python
# This node send twist msg to regulate the drone in position on the x axis.
#The servo point can be mobile  

from concurrent.futures import thread
from telnetlib import LOGOUT
import threading
import rospy
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist

x_drone1 = y_drone1 = z_drone1 = x_drone2  = y_drone2 = z_drone2 = 0.0


##PID SETTINGS##
TIME_STEP = 0.01
Kp = 1
Kd = 0
Ki = 0  
MAX_VAR =  1.0
MIN_VAR = -1.0
##############

class PID():
	def __init__(self,KP,KI,KD,target = 0):
		self.kp = KP
		self.ki = KI
		self.kd = KD		
		self.sp = target
		self.error_last = 0
		self.integral_error = 0
		self.saturation_max = None
		self.saturation_min = None
	def compute(self,pos,dt):
		error = self.sp - pos #compute the error
		derivative_error = (error - self.error_last) / dt #find the derivative of the error (how the error changes with time)
		self.integral_error += error * dt #error build up over time
		output = self.kp*error + self.ki*self.integral_error + self.kd*derivative_error 
		self.error_last = error
		if output > self.saturation_max and self.saturation_max is not None:
			output = self.saturation_max
		elif output < self.saturation_min and self.saturation_min is not None:
			output = self.saturation_min
		return output
	def setLims(self,min,max):
		self.saturation_max = max
		self.saturation_min = min


def callback1(data):

    global x_drone2 

    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    cmd = Twist()
    
    pid = PID(Kp,Ki,Kd, x_drone2)
    pid.setLims(MIN_VAR,MAX_VAR)

    cmd.linear.x = -1 * pid.compute(data.pose.position.x, TIME_STEP)
    rospy.loginfo("commande : %s" %str(-1 *pid.compute(data.pose.position.x, TIME_STEP)))
    pub.publish(cmd)
        


def callback2(data):
    global x_drone2
    global y_drone2
    global z_drone2

    x_drone2 = data.pose.position.x
    y_drone2 = data.pose.position.y
    z_drone2 = data.pose.position.z
    


def regul():

    rospy.init_node('regul_X_PID', anonymous=True)

    sub1 = rospy.Subscriber('/vrpn_client_node/Tello01/pose', PoseStamped, callback1)
    sub2 = rospy.Subscriber('/vrpn_client_node/Tello02/pose', PoseStamped, callback2)

    rospy.spin()

if __name__ == '__main__':
    regul()