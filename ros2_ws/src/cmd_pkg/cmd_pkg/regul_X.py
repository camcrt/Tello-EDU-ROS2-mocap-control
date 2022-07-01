
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist




x_drone = 0.0

class Regul_X(Node):
   
    

    def __init__(self):
        super().__init__('regul_X')


        self.subscription = self.create_subscription(
            PoseStamped,
            '/vrpn_client_node/Tello01/pose',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 0.001  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def listener_callback(self, data):
        global x_drone
        x_drone = data.pose.position.x
        #self.get_logger().info("tst")




    def timer_callback(self):
        
        global x_drone

        self.get_logger().info(str(x_drone))

        cmd = Twist()

    

        delta = 0.5
        x_wanted = 0.0

        if x_wanted - delta < x_drone < x_wanted + delta : 
            cmd.linear.x = 0.0
            self.publisher_.publish(cmd)
            return

        if x_drone > x_wanted + delta : 
            cmd.linear.x =   0.5
            self.publisher_.publish(cmd)

        if x_drone < x_wanted - delta: 
            cmd.linear.x =  - 0.5
            self.publisher_.publish(cmd)
        
        self.publisher_.publish(cmd)
        
        self.i += 1



def main(args=None):
    rclpy.init(args=args)

    regul_x = Regul_X()
    

    rclpy.spin(regul_x)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)

    regul_x.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()