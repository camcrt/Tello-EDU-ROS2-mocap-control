
from concurrent.futures import thread
import threading
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist

x_esclave = y_esclave = z_esclave = 0.0
x_ref = y_ref = z_ref = 0.0


TIME_STEP = 0.01
Kp = 1
Kd = 0
Ki = 0  
MAX_VAR =  1.0
MIN_VAR = -1.0


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



class Regul_pos(Node):
   
    

    def __init__(self):
        super().__init__('regul_pos')


        self.subscription_esclave = self.create_subscription(
            PoseStamped,
            '/vrpn_client_node/Tello01/pose',
            self.listener_callback_esclave,
            10)
        self.subscription_esclave  # prevent unused variable warning


        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 0.001  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.declare_parameter('position_x',0.0)
        self.declare_parameter('position_y',0.0)
        self.declare_parameter('position_z',0.0)
        

    def listener_callback_esclave(self, data):
        global x_esclave
        global y_esclave
        global z_esclave
        
        x_esclave = data.pose.position.x
        y_esclave = data.pose.position.y
        z_esclave = data.pose.position.z
        


    def timer_callback(self):
        
        cmd = Twist()

        def regul_x():

            global x_esclave
            global x_ref

            x_ref = self.get_parameter('position_x').value 

            #self.get_logger().info(str(z_drone))
            self.get_logger().info(str(x_ref))

            pid = PID(Kp,Ki,Kd, x_ref)
            pid.setLims(MIN_VAR,MAX_VAR)

            cmd.linear.y = -1 *( pid.compute(x_esclave, TIME_STEP))
            self.publisher_.publish(cmd)
            self.get_logger().info(("commande : %s" %str(pid.compute(x_esclave, TIME_STEP))))

        def regul_y():

            global y_esclave
            global y_ref

            y_ref = self.get_parameter('position_y').value 

            #self.get_logger().info(str(z_drone))
            self.get_logger().info(str(y_ref))

            pid = PID(Kp,Ki,Kd, y_ref)
            pid.setLims(MIN_VAR,MAX_VAR)

            cmd.linear.y = -1 *( pid.compute(y_esclave, TIME_STEP))
            self.publisher_.publish(cmd)
            self.get_logger().info(("commande : %s" %str(pid.compute(y_esclave, TIME_STEP))))
     

        def regul_z():

            global z_esclave
            global z_ref

            z_ref = self.get_parameter('position_z').value 

            #self.get_logger().info(str(z_drone))
            self.get_logger().info(str(z_ref))

            pid = PID(Kp,Ki,Kd, z_ref)
            pid.setLims(MIN_VAR,MAX_VAR)

            cmd.linear.z = pid.compute(z_esclave, TIME_STEP)
            self.publisher_.publish(cmd)
            self.get_logger().info(("commande : %s" %str(pid.compute(z_esclave, TIME_STEP))))

        t1 = threading.Thread(target=regul_x)
        t2 = threading.Thread(target=regul_y)
        t3 = threading.Thread(target=regul_z)

        t1.daemon = True
        t2.daemon = True
        t3.daemon = True
        
        t1.start()
        t2.start()
        t3.start()

def main(args=None):
    rclpy.init(args=args)

    regul_pos = Regul_pos()
    

    rclpy.spin(regul_pos)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)

    regul_pos.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()