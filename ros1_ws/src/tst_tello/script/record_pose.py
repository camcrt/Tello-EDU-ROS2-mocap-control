#!/usr/bin/env python
## Simple talker demo that listens to geometry_msgs/Pose published 
## to the '/vrpn_client_node/Tello01/pose' topic

import time
from asyncore import write
from concurrent.futures import thread
from math import dist
import threading
from turtle import delay, position
import rospy
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
import csv
from time import sleep
from datetime import datetime

header = ['time', 'x', 'y', 'z']

x_drone1 = y_drone1 = z_drone1 = x_drone2  = y_drone2 = z_drone2 = 0.0


def callback1(data):
    global x_drone1
    global y_drone1
    global z_drone1

    x_drone1 = data.pose.position.x 
    y_drone1 = data.pose.position.y 
    z_drone1 = data.pose.position.z

    # t1 = threading.Thread(target=rec)
    # t1.daemon = True
    # t1.start()
    # t1.join()



def callback2(data):
    global x_drone2
    global y_drone2
    global z_drone2

    x_drone2 = data.pose.position.x
    y_drone2 = data.pose.position.y
    z_drone2 = data.pose.position.z


    
def get_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def rec():
    
    
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    while True :

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        writer.writerow(header)
        
        sleep(0.5)
        rospy.loginfo("tst")


def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.

   
    rospy.init_node('record_pose', anonymous=True)
    
    #pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    sub1 = rospy.Subscriber('/vrpn_client_node/Tello01/pose', PoseStamped, callback1)
    sub2 = rospy.Subscriber('/vrpn_client_node/Tello02/pose', PoseStamped, callback2)

    def record():
       global z_drone1
       global x_drone1
       global y_drone1
        
       with open('eggs.csv', 'w', newline='') as csvfile:
           spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
           spamwriter.writerow(header)
           x=0
           y=0
           z=0 
            
           while True:
               if round(x_drone1,1) != round(x,2) or round(y_drone1,2) != round(y,2) or round(z_drone1,2) != round(z,2) :
                    x = x_drone1
                    y = y_drone1
                    z = z_drone1

                    spamwriter.writerow([get_time(), x, y, z])
                    sleep(0.01)


    t1 = threading.Thread(target = record)
    t1.daemon = True
    t1.start()
        


    # spin() simply keeps python from exiting until this node is stopped
    
    rospy.spin()

if __name__ == '__main__':
    listener()