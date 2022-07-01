source /opt/ros/foxy/setup.bash

sudo apt install libasio-dev
sudo apt install ros-foxy-cv-bridge ros-foxy-camera-calibration-parsers

cd src/
#Tello driver installation
git clone https://github.com/clydemcqueen/tello_ros.git
git clone https://github.com/ptrmu/ros2_shared.git


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
