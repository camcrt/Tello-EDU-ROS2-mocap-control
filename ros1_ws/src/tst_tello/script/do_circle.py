#!/usr/bin/env python
# Do a circle by sending twist message just for checking if the /cmd_vel topic is enable
import rospy
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
def callback(data):
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    cmd = Twist()
    cmd.linear.x = 0.2
    cmd.angular.z = 0.5
    pub.publish(cmd)
    
    
    


def circle():

    rospy.init_node('make_circle', anonymous=True)

    sub = rospy.Subscriber('/vrpn_client_node/Tello01/pose', PoseStamped, callback)
    rospy.spin()

if __name__ == '__main__':
    circle()
    