
from glob import glob
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Pose
from geometry_msgs.msg import Twist

z_ref = 1.0
x_ref = 1.0
y_ref = 1.0



class Ref_Input(Node):
   
    

    def __init__(self):
        super().__init__('ref_input')

        self.publisher_ = self.create_publisher(Pose, '/pos_ref', 10)
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
       

    def timer_callback(self):
        
        global z_ref
        
        pose = Pose()
        #pose.header.frame_id = "position_z"
        while rclpy.ok() :    
            pose.position.z = input("z = " )
            #pose.header.stamp = ref_input.get_clock().now()
            self.publisher_.publish(pose)
            

def main(args=None):
    rclpy.init(args=args)

    ref_input = Ref_Input()
    

    rclpy.spin(ref_input)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)

    ref_input.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()