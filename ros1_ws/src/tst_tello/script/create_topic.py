#!/usr/bin/env python
## Create some topic to use them in rqt_plot

import rospy
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

def callback1(data):
    
    pub1 = rospy.Publisher("/pos/x/esclave", Float32, queue_size=10)
    pub1.publish(data.pose.position.x) 

    pub2 = rospy.Publisher("/pos/y/esclave", Float32, queue_size=10)
    pub2.publish(data.pose.position.y)

    pub3 = rospy.Publisher("/pos/z/esclave", Float32, queue_size=10)
    pub3.publish(data.pose.position.z)


def callback2(data):
    
    pub1 = rospy.Publisher("/pos/x/maitre", Float32, queue_size=10)
    pub1.publish(data.pose.position.x) 

    pub2 = rospy.Publisher("/pos/y/maitre", Float32, queue_size=10)
    pub2.publish(data.pose.position.y)

    pub3 = rospy.Publisher("/pos/z/maitre", Float32, queue_size=10)
    pub3.publish(data.pose.position.z)


def listener():

    
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('/vrpn_client_node/Tello01/pose', PoseStamped, callback1)
    rospy.Subscriber('/vrpn_client_node/Tello02/pose', PoseStamped, callback2)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
