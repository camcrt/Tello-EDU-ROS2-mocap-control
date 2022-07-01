
from tkinter import Y
from zlib import ZLIB_VERSION
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
import threading


x_drone_maitre = y_drone_maitre = z_drone_maitre = 0.0
x_drone_esclave = y_drone_esclave = z_drone_esclave = 0.0
x_twist = y_twist = z_twist = 0

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


class Drone_suiveur_PID(Node):

    def __init__(self):
        super().__init__('drone_suiveur_PID')


        self.subscription_maitre = self.create_subscription(
            PoseStamped,
            '/vrpn_client_node/Tello02/pose',
            self.listener_callback_maitre,
            10)
        self.subscription_maitre  # prevent unused variable warning

        self.subscription_esclave = self.create_subscription(
            PoseStamped,
            '/vrpn_client_node/Tello01/pose',
            self.listener_callback_esclave,
            10)
        self.subscription_esclave

        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 0.001  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def listener_callback_maitre(self, data):
        global x_drone_maitre
        global y_drone_maitre
        global z_drone_maitre

        x_drone_maitre = data.pose.position.x
        y_drone_maitre = data.pose.position.y
        z_drone_maitre = data.pose.position.z

    
    def listener_callback_esclave(self, data):
        global x_drone_esclave
        global y_drone_esclave
        global z_drone_esclave

        x_drone_esclave = data.pose.position.x
        y_drone_esclave = data.pose.position.y
        z_drone_esclave = data.pose.position.z


    def timer_callback(self):
        global x_twist
        global y_twist
        global z_twist
        
        global x_drone_maitre
        global y_drone_maitre
        global z_drone_maitre
        
        global x_drone_esclave
        global y_drone_esclave
        global z_drone_esclave

        cmd = Twist()

        def regul_x():
            global x_twist

            pid_x = PID(Kp_x,Ki_x,Kd_x, x_drone_maitre + 1)
            pid_x.setLims(MIN_VAR,MAX_VAR)

            x_twist = -1 * pid_x.compute(x_drone_esclave, TIME_STEP)
            self.publisher_.publish(cmd)
            #self.get_logger().info(("commande : %s" %str(cmd.linear.x)))

           
        def regul_y():
            global y_twist

            pid_y = PID(Kp_y,Ki_y,Kd_y, y_drone_maitre)
            pid_y.setLims(MIN_VAR,MAX_VAR)

            y_twist = -1 * pid_y.compute(y_drone_esclave, TIME_STEP)
            self.publisher_.publish(cmd)
            #self.get_logger().info(("commande : %s" %str(cmd.linear.y)))

           
    
        def regul_z():
            global z_twist

            pid_z = PID(Kp_z,Ki_z,Kd_z, z_drone_maitre)
            pid_z.setLims(MIN_VAR,MAX_VAR)

            z_twist = pid_z.compute(z_drone_esclave, TIME_STEP)
            #self.get_logger().info(("commande : %s" %str(cmd.linear.z)))
    
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


        cmd.linear.x = x_twist
        cmd.linear.y = y_twist
        cmd.linear.z = z_twist

        self.publisher_.publish(cmd)

        self.i += 1



def main(args=None):
    rclpy.init(args=args)
    drone_suiveur_PID = Drone_suiveur_PID()

    rclpy.spin(drone_suiveur_PID)

    drone_suiveur_PID.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()