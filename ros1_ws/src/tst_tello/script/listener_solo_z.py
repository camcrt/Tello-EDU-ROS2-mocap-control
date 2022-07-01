#!/usr/bin/env python
## Simple talker demo that listens to geometry_msgs/Pose published 
## to the '/vrpn_client_node/Tello01/pose' topic

import rospy
from geometry_msgs.msg import PoseStamped

def callback(data):
    #rospy.loginfo(data)
    #rospy.loginfo(data.pose.position)
    rospy.loginfo(data.pose.position.z)


def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('/vrpn_client_node/Tello01/pose', PoseStamped, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
