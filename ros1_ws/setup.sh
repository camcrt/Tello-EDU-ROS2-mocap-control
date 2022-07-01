sudo apt-get install ros-noetic-vrpn-client-ros
source /opt/ros/noetic/setup.bash
cd src/

#VRPN package Installation
git clone https://github.com/ros-drivers/vrpn_client_ros.git
cd ..

# #regulation and tools package
# git clone https://github.com/camcrt/tst_Tello.git

catkin_make 
source devel/setup.bash