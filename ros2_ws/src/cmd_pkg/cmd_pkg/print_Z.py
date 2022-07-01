#publie un pose stamped

from glob import glob
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist

z_ref = 1.0
x_ref = 1.0
y_ref = 1.0



class Ref_Input(Node):
   
    

    def __init__(self):
        super().__init__('ref_input')

        self.publisher_ = self.create_publisher(PoseStamped, '/pos_ref', 10)
       

    def get_loop(self):
        
        global z_ref
        
        pose = PoseStamped()
        pose.header.frame_id = "position_z"
        while rclpy.ok() :    
            pose.pose.position.z = input("z = " )
            pose.header.stamp = ref_input.get_clock().now()
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