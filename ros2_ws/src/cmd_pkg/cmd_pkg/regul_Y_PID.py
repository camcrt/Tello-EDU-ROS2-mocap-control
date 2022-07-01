
from glob import escape
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist

y_esclave = y_maitre = 0.0


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



class regul_Y_PID(Node):
   
    

    def __init__(self):
        super().__init__('regul_Y_PID')


        self.subscription_esclave = self.create_subscription(
            PoseStamped,
            '/vrpn_client_node/Tello01/pose',
            self.listener_callback_esclave,
            10)
        self.subscription_esclave  # prevent unused variable warning

        self.subscription_maitre = self.create_subscription(
            PoseStamped,
            '/vrpn_client_node/Tello02/pose',
            self.listener_callback_maitre,
            10)
        self.subscription_maitre  # prevent unused variable warning

        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 0.001  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def listener_callback_esclave(self, data):
        global y_esclave
        y_esclave = data.pose.position.y
        #self.get_logger().info("tst")

    def listener_callback_maitre(self, data):
        global y_maitre
        y_maitre = data.pose.position.y
        #self.get_logger().info("tst")

    



    def timer_callback(self):
        
        global y_esclave
        global y_maitre

        #self.get_logger().info(str(z_drone))

        cmd = Twist()

        pid = PID(Kp,Ki,Kd, y_maitre + 1)
        pid.setLims(MIN_VAR,MAX_VAR)

        cmd.linear.y = -1 * pid.compute(y_esclave, TIME_STEP)
        self.publisher_.publish(cmd)
        self.get_logger().info(("commande : %s" %str(cmd.linear.y)))
        self.i += 1



def main(args=None):
    rclpy.init(args=args)

    regul_y_pid = regul_Y_PID()
    

    rclpy.spin(regul_y_pid)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)

    regul_y_pid.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()