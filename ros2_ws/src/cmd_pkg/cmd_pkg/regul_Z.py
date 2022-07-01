
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist




z_drone = 0.0

class Regul_Z(Node):
   
    

    def __init__(self):
        super().__init__('regul_Z')


        self.subscription = self.create_subscription(
            PoseStamped,
            '/vrpn_client_node/Tello02/pose',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.publisher_ = self.create_publisher(Twist, '/drone1/control', 10)
        timer_period = 0.001  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def listener_callback(self, data):
        global z_drone
        z_drone = data.pose.position.z
        #self.get_logger().info("tst")




    def timer_callback(self):
        
        global z_drone

        self.get_logger().info(str(z_drone))

        cmd = Twist()

    

        delta = 0.10
        z_wanted = 1.0

        if z_wanted - delta < z_drone < z_wanted + delta : 
            cmd.linear.z = 0.0
            self.publisher_.publish(cmd)
            return

        if z_drone > z_wanted + delta : 
            cmd.linear.z = -30.0
            self.publisher_.publish(cmd)

        if z_drone < z_wanted - delta: 
            cmd.linear.z = 30.0
            self.publisher_.publish(cmd)
        
        self.publisher_.publish(cmd)
        
        self.i += 1



def main(args=None):
    rclpy.init(args=args)

    regul_z = Regul_Z()
    

    rclpy.spin(regul_z)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)

    regul_z.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()