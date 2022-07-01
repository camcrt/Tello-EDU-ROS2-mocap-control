 #!/usr/bin/env python
## Simple talker demo that listens to geometry_msgs/Pose published 
## to the '/vrpn_client_node/Tello01/pose' topic

from concurrent.futures import thread
from math import dist
import threading
import rospy
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist

x_drone1 = y_drone1 = z_drone1 = x_drone2  = y_drone2 = z_drone2 = 0.0

TIME_STEP = 0.01
MAX_VAR =  1.0
MIN_VAR = -1.0

Kp_x = 1
Kd_x = 0
Ki_x = 0  

Kp_y = 1
Kd_y = 0
Ki_y = 0  

Kp_z = 1
Kd_z = 0
Ki_z = 0

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
    global y_drone2
    global z_drone2 

    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    cmd = Twist()
    
    def regul_x():
        global x_drone2 

        pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        cmd = Twist()
    
        pid = PID(Kp_x,Ki_x,Kd_x, x_drone2)
        pid.setLims(MIN_VAR,MAX_VAR)

        cmd.linear.x = -1 * pid.compute(data.pose.position.x, TIME_STEP)
        rospy.loginfo("commande : %s" %str(-1 *pid.compute(data.pose.position.x, TIME_STEP)))
        pub.publish(cmd)


    def regul_y():
        global y_drone2 

        pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        cmd = Twist()
    
        pid = PID(Kp_y,Ki_y,Kd_y, y_drone2 + 1)
        pid.setLims(MIN_VAR,MAX_VAR)

        cmd.linear.y = -1 * pid.compute(data.pose.position.y, TIME_STEP)
        rospy.loginfo("commande : %s" %str(-1 *pid.compute(data.pose.position.y, TIME_STEP)))
        pub.publish(cmd)

    def regul_z():
        global z_drone2 

        pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        cmd = Twist()
    

        pid = PID(Kp_z,Ki_z,Kd_z, z_drone2)
        pid.setLims(MIN_VAR,MAX_VAR)

        cmd.linear.z = pid.compute(data.pose.position.z, TIME_STEP)
        rospy.loginfo("commande : %s" %str(pid.compute(data.pose.position.z, TIME_STEP)))
        pub.publish(cmd)
    
    
    t1 = threading.Thread(target=regul_x)
    t2 = threading.Thread(target=regul_y)
    t3 = threading.Thread(target=regul_z)

    t1.daemon = True
    t2.daemon = True
    t3.daemon = True

    t1.start()
    t2.start()
    t3.start()

    t1.join()

    t2.join()
    t3.join() 

    

    




def callback2(data):
    global x_drone2
    global y_drone2
    global z_drone2

    x_drone2 = data.pose.position.x
    y_drone2 = data.pose.position.y
    z_drone2 = data.pose.position.z
    


def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.

   
    rospy.init_node('regul_X', anonymous=True)

    #pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    sub1 = rospy.Subscriber('/vrpn_client_node/Tello01/pose', PoseStamped, callback1)
    sub2 = rospy.Subscriber('/vrpn_client_node/Tello02/pose', PoseStamped, callback2)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()