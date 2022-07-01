#!/usr/bin/env python
## Simple talker demo that listens to geometry_msgs/Pose published 
## to the '/vrpn_client_node/Tello01/pose' topic

from concurrent.futures import thread
import threading
import rospy
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist

x_drone1 = y_drone1 = z_drone1 = x_drone2  = y_drone2 = z_drone2 = 0.0


def callback1(data):

    global x_drone2
    global y_drone2
    global z_drone2 

    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    cmd = Twist()

    delta = 0.1

    
    def regul_x():

        delta = 0.1

        

        if x_drone2 - delta < data.pose.position.x < x_drone2 + delta : 
            cmd.linear.x = 0
            pub.publish(cmd)
            return

        if data.pose.position.x > x_drone2 + delta : 
            cmd.linear.x = 0.5
            pub.publish(cmd)

        if data.pose.position.x < x_drone2 - delta: 
            cmd.linear.x = -0.5
            pub.publish(cmd)

        pub.publish(cmd)

        if x_drone2 - delta < data.pose.position.x < x_drone2 + delta : 
            cmd.linear.x = 0
            pub.publish(cmd)
            return

        if data.pose.position.x > x_drone2 + delta : 
            cmd.linear.x = 0.5
            pub.publish(cmd)

        if data.pose.position.x < x_drone2 - delta: 
            cmd.linear.x = -0.5
            pub.publish(cmd)

        pub.publish(cmd)

    def regul_y():
        global y_drone2


        delta = 0.1

        if y_drone2 - delta < data.pose.position.y < y_drone2 + delta : 
            cmd.linear.y = 0
            pub.publish(cmd)
            return

        if data.pose.position.y > y_drone2 + delta : 
            cmd.linear.y = 0.5
            pub.publish(cmd)

        if data.pose.position.y < y_drone2 - delta: 
            cmd.linear.y = -0.5
            pub.publish(cmd)

        pub.publish(cmd)

        if y_drone2 - delta < data.pose.position.y < y_drone2 + delta : 
            cmd.linear.y = 0
            pub.publish(cmd)
            return

        if data.pose.position.y > y_drone2 + delta : 
            cmd.linear.y = 0.5
            pub.publish(cmd)

        if data.pose.position.y < y_drone2 - delta: 
            cmd.linear.y = -0.5
            pub.publish(cmd)

        pub.publish(cmd)

    def regul_z():
        global z_drone2


        delta = 0.1

        if z_drone2 - delta < data.pose.position.z < z_drone2 + delta : 
            cmd.linear.z = 0
            pub.publish(cmd)
            return

        if data.pose.position.z < z_drone2 - delta : 
            cmd.linear.z = 0.5
            pub.publish(cmd)

        if data.pose.position.z > z_drone2 + delta: 
            cmd.linear.z = -0.5
            pub.publish(cmd)

        pub.publish(cmd)
    
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

    

    




def callback2(data):
    global x_drone2
    global y_drone2
    global z_drone2

    x_drone2 = data.pose.position.x
    y_drone2 = data.pose.position.y
    z_drone2 = data.pose.position.z
    


def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.

   
    rospy.init_node('regul_X', anonymous=True)

    #pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    sub1 = rospy.Subscriber('/vrpn_client_node/Tello01/pose', PoseStamped, callback1)
    sub2 = rospy.Subscriber('/vrpn_client_node/Tello02/pose', PoseStamped, callback2)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()