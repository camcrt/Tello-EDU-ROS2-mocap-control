#!/usr/bin/env python
## Simple talker demo that listens to geometry_msgs/Pose published 
## to the '/vrpn_client_node/Tello01/pose' topic

import rospy
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
def callback(data):

    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    cmd = Twist()

    delta = 0.1

    if -0.1 - delta < data.pose.position.y < -0.1 + delta : 
        cmd.linear.y = 0
        pub.publish(cmd)
        return

    if data.pose.position.y > -0.1 + delta : 
        cmd.linear.y = 0.5
        pub.publish(cmd)

    if data.pose.position.y < -0.1 - delta: 
        cmd.linear.y = -0.5
        pub.publish(cmd)

    pub.publish(cmd)
    
    


def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.

   
    rospy.init_node('regul_Y', anonymous=True)

    #pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    sub = rospy.Subscriber('/vrpn_client_node/Tello01/pose', PoseStamped, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()