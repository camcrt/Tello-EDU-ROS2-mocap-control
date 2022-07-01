
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
import threading


x_drone_maitre = y_drone_maitre = z_drone_maitre = 0.0
x_drone_esclave = y_drone_esclave = z_drone_esclave = 0.0

class Drone_suiveur(Node):
   
    

    def __init__(self):
        super().__init__('drone_suiveur')


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
        
        global x_drone_maitre
        global y_drone_maitre
        global z_drone_maitre
        
        global x_drone_esclave
        global y_drone_esclave
        global z_drone_esclave

        cmd = Twist()

        def regul_x():

            delta = 0.3
            distance = 1

            if distance - delta < x_drone_esclave - x_drone_maitre  < distance + delta :
                cmd.linear.x = 0.0
                self.publisher_.publish(cmd)
                return

            if x_drone_esclave - x_drone_maitre > distance + delta : 
                cmd.linear.x = 0.5
                self.publisher_.publish(cmd)

            if x_drone_esclave - x_drone_maitre < distance - delta : 
                cmd.linear.x = - 0.5
                self.publisher_.publish(cmd)

            self.publisher_.publish(cmd)


        def regul_y():

            delta = 0.4
            distance = 0.5

            if y_drone_maitre - delta  < y_drone_esclave< y_drone_maitre + delta :
                cmd.linear.y = 0.0
                self.publisher_.publish(cmd)
                return

            if y_drone_esclave> y_drone_maitre + delta : 
                cmd.linear.y = 0.5
                self.publisher_.publish(cmd)

            if y_drone_esclave< y_drone_maitre - delta : 
                cmd.linear.y = -0.5
                self.publisher_.publish(cmd)

    

        def regul_z():

            delta = 0.1

            if z_drone_maitre - delta < z_drone_esclave < z_drone_maitre + delta : 
                cmd.linear.z = 0.0
                self.publisher_.publish(cmd)
                return

            if z_drone_esclave < z_drone_maitre - delta : 
                cmd.linear.z = 0.5
                self.publisher_.publish(cmd)

            if z_drone_esclave > z_drone_maitre + delta: 
                cmd.linear.z = -0.5
                self.publisher_.publish(cmd)

            self.publisher_.publish(cmd)
    
    
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

        
        self.i += 1



def main(args=None):
    rclpy.init(args=args)

    drone_suiveur = Drone_suiveur()
    

    rclpy.spin(drone_suiveur)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)

    drone_suiveur.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()