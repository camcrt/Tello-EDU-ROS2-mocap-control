source /opt/ros/foxy/setup.bash

sudo apt install libasio-dev
sudo apt install ros-foxy-cv-bridge ros-foxy-camera-calibration-parsers

cd src/
#Tello driver dependencies

pip3 install catkin_pkg rospkg av image opencv-python djitellopy2 pyyaml
sudo apt install python3-tf*
sudo apt install ros-foxy-ament-cmake* ros-foxy-tf2* ros-foxy-rclcpp* ros-foxy-rosgraph*
sudo apt install ros-foxy-rviz* ros-foxy-rqt*


# #regulation and tools package
# git clone https://github.com/camcrt/cmd_pkg.git

#building packages
cd ..
colcon build 
source install/setup.bash

#ROS1-ROS2 bridge
source /opt/ros/noetic/setup.bash
source /opt/ros/foxy/setup.bash
cd src/
git clone https://github.com/ros2/ros1_bridge.git
cd ..
colcon build --symlink-install --packages-select ros1_bridge --cmake-force-configure
source install/setup.bash
