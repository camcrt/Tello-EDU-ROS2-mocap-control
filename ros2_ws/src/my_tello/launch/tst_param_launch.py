from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_tello',
            executable='test_param',
            name='test_param',
            output='screen',
            emulate_tty=True,
            parameters=[
                {'tello_ip': '192.168.43.22'}
            ]
        )
    ])