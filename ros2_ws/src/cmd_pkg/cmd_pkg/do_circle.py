#!/usr/bin/env python3

import pprint
import math
import rclpy
import threading
import numpy
import time
import av
import tf2_ros
import cv2
import time
import yaml
from conf import *
from djitellopy import TelloSwarm

from rclpy.node import Node
from tello_msg.msg import TelloStatus, TelloID, TelloWifiConfig
from std_msgs.msg import Empty, UInt8, UInt8, Bool, String
from sensor_msgs.msg import Image, Imu, BatteryState, Temperature, CameraInfo
from geometry_msgs.msg import Twist, TransformStamped
from nav_msgs.msg import Odometry
from cv_bridge import CvBridge
import ament_index_python

class Create_tello(rclpy.node.Node):
    def __init__(self, node):
        self.node = node

        # Connect to drone
        
        self.conf = Configuration('router name', 'SSID', 'password', 24)
        self.ip_tellos = conf.getTelloIp()
        self.node.get_logger().info('Tello: Connecting to drone')

        self.swarm = TelloSwarm.fromIps(self.ip_tellos)

        self.swarm.connect()
        self.swarm.takeoff()


        self.node.get_logger().info('Tellos are connected')

        # Publishers and subscribers
        self.setup_publishers()
        self.setup_subscribers()

        # Processing threads
        self.start_tello_status()
        self.start_tello_odom()

        self.node.get_logger().info('Tello: Driver node ready')

    # Setup ROS publishers of the node.
    def setup_publishers(self):
        self.pub_status = self.node.create_publisher(TelloStatus, 'status', 1)
        self.pub_id = self.node.create_publisher(TelloID, 'id', 1)
        self.pub_imu = self.node.create_publisher(Imu, 'imu', 1)
        self.pub_battery = self.node.create_publisher(BatteryState, 'battery', 1)
        self.pub_temperature = self.node.create_publisher(Temperature, 'temperature', 1)
        self.pub_odom = self.node.create_publisher(Odometry, 'odom', 1)

        # TF broadcaster
        if self.tf_pub:
            self.tf_broadcaster = tf2_ros.TransformBroadcaster(self.node)
    
    # Setup the topic subscribers of the node.
    def setup_subscribers(self):
        self.sub_emergency = self.node.create_subscription(Empty, 'emergency', self.cb_emergency, 1)
        self.sub_takeoff = self.node.create_subscription(Empty, '/drone1/takeoff', self.cb_takeoff1, 1)
        self.sub_takeoff = self.node.create_subscription(Empty, '/drone2/takeoff', self.cb_takeoff2, 1)
        self.sub_land = self.node.create_subscription(Empty, '/drone1/land', self.cb_land1, 1)
        self.sub_land = self.node.create_subscription(Empty, '/drone2/land', self.cb_land2, 1)
        self.sub_control = self.node.create_subscription(Twist, '/drone1/control', self.cb_control1, 1)
        self.sub_control = self.node.create_subscription(Twist, '/drone2/control', self.cb_control2, 1)
        self.sub_flip = self.node.create_subscription(String, 'flip', self.cb_flip, 1)
        self.sub_wifi_config = self.node.create_subscription(TelloWifiConfig, 'wifi_config', self.cb_wifi_config, 1)

    # Start drone info thread
    def start_tello_odom(self, rate=1.0/10.0):
        def status_odom():
            while True:
                # TF
                if self.tf_pub:
                    t = TransformStamped()
                    t.header.stamp = self.node.get_clock().now().to_msg()
                    t.header.frame_id = self.tf_base
                    t.child_frame_id = self.tf_drone
                    t.transform.translation.x = 0.0
                    t.transform.translation.y = 0.0
                    t.transform.translation.z = (self.tello.get_barometer()) / 100.0
                    self.tf_broadcaster.sendTransform(t)
                
                # IMU
                if self.pub_imu.get_subscription_count() > 0:
                    q = self.get_orientation_quaternion()

                    msg = Imu()
                    msg.header.stamp = self.node.get_clock().now().to_msg()
                    msg.header.frame_id = self.tf_drone
                    msg.linear_acceleration.x = self.tello.get_acceleration_x() / 100.0
                    msg.linear_acceleration.y = self.tello.get_acceleration_y() / 100.0
                    msg.linear_acceleration.z = self.tello.get_acceleration_z() / 100.0
                    msg.orientation.x = q[0]
                    msg.orientation.y = q[1]
                    msg.orientation.z = q[2]
                    msg.orientation.w = q[3]
                    self.pub_imu.publish(msg)

                # Odometry
                if self.pub_odom.get_subscription_count() > 0:
                    q = self.get_orientation_quaternion()

                    odom_msg = Odometry()
                    odom_msg.header.stamp = self.node.get_clock().now().to_msg()
                    odom_msg.header.frame_id = self.tf_base
                    odom_msg.pose.pose.orientation.x = q[0]
                    odom_msg.pose.pose.orientation.y = q[1]
                    odom_msg.pose.pose.orientation.z = q[2]
                    odom_msg.pose.pose.orientation.w = q[3]
                    odom_msg.twist.twist.linear.x = float(self.tello.get_speed_x()) / 100.0
                    odom_msg.twist.twist.linear.y = float(self.tello.get_speed_y()) / 100.0
                    odom_msg.twist.twist.linear.z = float(self.tello.get_speed_z()) / 100.0
                    self.pub_odom.publish(odom_msg)
                
                time.sleep(rate)

        thread = threading.Thread(target=status_odom)
        thread.start()
        return thread

    # Start drone info thread
    def start_tello_status(self, rate=1.0/2.0):
        def status_loop():
            while True:
                # Battery
                if self.pub_battery.get_subscription_count() > 0:
                    msg = BatteryState()
                    msg.header.frame_id = self.tf_drone
                    msg.percentage = float(self.tello.get_battery())
                    msg.voltage = 3.8
                    msg.design_capacity = 1.1
                    msg.present = True
                    msg.power_supply_technology = 2 # POWER_SUPPLY_TECHNOLOGY_LION
                    msg.power_supply_status = 2 # POWER_SUPPLY_STATUS_DISCHARGING
                    self.pub_battery.publish(msg)

                # Temperature
                if self.pub_temperature.get_subscription_count() > 0:
                    msg = Temperature()
                    msg.header.frame_id = self.tf_drone
                    msg.temperature = self.tello.get_temperature()
                    msg.variance = 0.0
                    self.pub_temperature.publish(msg)

                # Tello Status
                if self.pub_status.get_subscription_count() > 0:
                    msg = TelloStatus()
                    msg.acceleration.x = self.tello.get_acceleration_x()
                    msg.acceleration.y = self.tello.get_acceleration_y()
                    msg.acceleration.z = self.tello.get_acceleration_z()

                    msg.speed.x = float(self.tello.get_speed_x())
                    msg.speed.y = float(self.tello.get_speed_y())
                    msg.speed.z = float(self.tello.get_speed_z())

                    msg.pitch = self.tello.get_pitch()
                    msg.roll = self.tello.get_roll()
                    msg.yaw = self.tello.get_yaw()

                    msg.barometer = int(self.tello.get_barometer())
                    msg.distance_tof = self.tello.get_distance_tof()

                    msg.fligth_time = self.tello.get_flight_time()

                    msg.battery = self.tello.get_battery()

                    msg.highest_temperature = self.tello.get_highest_temperature()
                    msg.lowest_temperature = self.tello.get_lowest_temperature()
                    msg.temperature = self.tello.get_temperature()

                    msg.wifi_snr = self.tello.query_wifi_signal_noise_ratio()

                    self.pub_status.publish(msg)

                # Tello ID
                if self.pub_id.get_subscription_count() > 0:
                    msg = TelloID()
                    msg.sdk_version = self.tello.query_sdk_version()
                    msg.serial_number = self.tello.query_serial_number()
                    self.pub_id.publish(msg)
                
                # Sleep
                time.sleep(rate)

        thread = threading.Thread(target=status_loop)
        thread.start()
        return thread


    # Terminate the code and shutdown node.
    def terminate(self, err):
        self.node.get_logger().error(str(err))
        self.tello.end()
        rclpy.shutdown()

    # Stop all movement in the drone
    def cb_emergency(self, msg):
        self.tello.emergency()

    # Drone takeoff message control
    def cb_takeoff1(self, msg):
        self.tello.takeoff()

    # Drone takeoff message control
    def cb_takeoff2(self, msg):
        self.tello2.takeoff()

    # Land the drone message callback
    def cb_land1(self, msg):
        self.tello.land()
    
    def cb_land2(self, msg):
        self.tello2.land()

    # Control messages received use to control the drone "analogically"
    #
    # This method of controls allow for more precision in the drone control.
    #
    # Receives the linear and angular velocities to be applied from -100 to 100.
    def cb_control1(self, msg):
        self.tello.send_rc_control(int(msg.linear.x), int(msg.linear.y), int(msg.linear.z), int(msg.angular.z))
    
    def cb_control2(self, msg):
        self.tello2.send_rc_control(int(msg.linear.x), int(msg.linear.y), int(msg.linear.z), int(msg.angular.z))

    # Configure the wifi credential that should be used by the drone.
    #
    # The drone will be restarted after the credentials are changed.
    def cb_wifi_config(self, msg):
        self.tello.set_wifi_credentials(msg.ssid, msg.password)
    
    # Perform a drone flip in a direction specified.
    # 
    # Directions can be "r" for right, "l" for left, "f" for forward or "b" for backward.
    def cb_flip(self, msg):
        self.tello.flip(msg.data)

# Convert a rotation from euler to quaternion.
def euler_to_quaternion(r):
    (yaw, pitch, roll) = (r[0], r[1], r[2])
    qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
    qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
    qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    return [qx, qy, qz, qw]

# Convert rotation from quaternion to euler.
def quaternion_to_euler(q):
    (x, y, z, w) = (q[0], q[1], q[2], q[3])
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(t0, t1)
    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch = math.asin(t2)
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(t3, t4)
    return [yaw, pitch, roll]


def main(args=None):
    rclpy.init(args=args)

    node = rclpy.create_node('tello')
    create_tello = Create_tello(node)

    rclpy.spin(node)

    create_tello.cb_shutdown()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()