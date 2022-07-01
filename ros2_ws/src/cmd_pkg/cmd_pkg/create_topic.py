
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

from geometry_msgs.msg import PoseStamped


x_drone_maitre = y_drone_maitre = z_drone_maitre = 0.0
x_drone_esclave = y_drone_esclave = z_drone_esclave = 0.0

class Create_topic(Node):
   
    

    def __init__(self):
        super().__init__('create_topic')


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

        self.publisher_x_maitre = self.create_publisher(Float32, '/pos/maitre/x', 10)
        self.publisher_y_maitre = self.create_publisher(Float32, '/pos/maitre/y', 10)
        self.publisher_z_maitre = self.create_publisher(Float32, '/pos/maitre/z', 10)

        self.publisher_x_esclave = self.create_publisher(Float32, '/pos/esclave/x', 10)
        self.publisher_y_esclave = self.create_publisher(Float32, '/pos/esclave/y', 10)
        self.publisher_z_esclave = self.create_publisher(Float32, '/pos/esclave/z', 10)
        
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

        global x_drone_maitre
        global y_drone_maitre
        global z_drone_maitre
        
        global x_drone_esclave
        global y_drone_esclave
        global z_drone_esclave

        info_x_maitre = Float32()
        info_y_maitre = Float32()
        info_z_maitre = Float32()

        info_x_esclave = Float32()
        info_y_esclave = Float32()
        info_z_esclave = Float32()
        
        info_x_maitre.data = x_drone_maitre
        info_y_maitre.data = y_drone_maitre 
        info_z_maitre.data = z_drone_maitre

        info_x_esclave.data = x_drone_esclave
        info_y_esclave.data = y_drone_esclave
        info_z_esclave.data = z_drone_esclave


        self.publisher_x_maitre.publish(info_x_maitre.data)
        self.publisher_y_maitre.publish(info_y_maitre.data)
        self.publisher_z_maitre.publish(info_z_maitre.data)

        self.publisher_x_esclave.publish(info_x_esclave.data)
        self.publisher_y_esclave.publish(info_y_esclave.data)
        self.publisher_z_esclave.publish(info_z_esclave.data)
        
        i += 1
        

def main(args=None):
    rclpy.init(args=args)

    create_topic = Create_topic()
    

    rclpy.spin(create_topic)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)

    create_topic.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()