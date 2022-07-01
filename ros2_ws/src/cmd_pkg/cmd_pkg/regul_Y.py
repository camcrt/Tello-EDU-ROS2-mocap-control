
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist




y_drone = 0.0

class Regul_Y(Node):
   
    

    def __init__(self):
        super().__init__('regul_Y')


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
        global y_drone
        y_drone = data.pose.position.y
        #self.get_logger().info("tst")




    def timer_callback(self):
        
        global y_drone

        self.get_logger().info(str(y_drone))

        cmd = Twist()

    

        delta = 0.3
        y_wanted = 0.0

        if y_wanted - delta < y_drone < y_wanted + delta : 
            cmd.linear.y = 0.0
            self.publisher_.publish(cmd)
            return

        if y_drone > y_wanted - delta : 
            cmd.linear.y =  0.5
            self.publisher_.publish(cmd)

        if y_drone < y_wanted + delta: 
            cmd.linear.y = - 0.5
            self.publisher_.publish(cmd)
        
        self.publisher_.publish(cmd)
        
        self.i += 1



def main(args=None):
    rclpy.init(args=args)

    regul_y = Regul_Y()
    

    rclpy.spin(regul_y)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)

    regul_y.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()