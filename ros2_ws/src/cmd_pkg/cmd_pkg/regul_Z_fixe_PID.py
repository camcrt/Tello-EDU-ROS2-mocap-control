
from glob import glob
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist

z_esclave =  0.0
z_ref = 1.0


TIME_STEP = 0.01
Kp = 200
Kd = 0
Ki = 5  
MAX_VAR =  100.0
MIN_VAR = -100.0


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



class regul_Z_fixe_PID(Node):
   
    

    def __init__(self):
        super().__init__('regul_Z_PID')

        self.declare_parameter('position_z', 1.0)
        
        self.subscription_esclave = self.create_subscription(
            PoseStamped,
            '/vrpn_client_node/Tello01/pose',
            self.listener_callback_esclave,
            10)
        self.subscription_esclave  # prevent unused variable warning

        self.subscription_z_ref = self.create_subscription(PoseStamped,'/z_ref',self.listener_z_ref,10)
        self.subscription_z_ref  # prevent unused variable warning

        self.publisher_ = self.create_publisher(Twist, '/drone1/control', 10)
        timer_period = 0.001  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        


    def listener_callback_esclave(self, data):
        global z_esclave
        z_esclave = data.pose.position.z
        #self.get_logger().info("tst")

    def listener_z_ref(self,data):
        global z_ref
        z_ref = data.pose.position.z


    def timer_callback(self):
        
        global z_esclave
        global z_ref

        #self.get_logger().info(str(z_drone))
        self.get_logger().info(str(z_ref))

        cmd = Twist()

        pid = PID(Kp,Ki,Kd, z_ref)
        pid.setLims(MIN_VAR,MAX_VAR)

        cmd.linear.z = pid.compute(z_esclave, TIME_STEP)
        self.publisher_.publish(cmd)
        self.get_logger().info(("commande : %s" %str(pid.compute(z_esclave, TIME_STEP))))
     



def main(args=None):
    rclpy.init(args=args)

    regul_z_fixe_pid = regul_Z_fixe_PID()
    

    rclpy.spin(regul_z_fixe_pid)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)

    regul_z_fixe_pid.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()