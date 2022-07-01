
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            
            package='my_tello',
            executable='create_tello',
            output='screen',
            namespace='/',
            name='tello1',
            parameters=[
                {'connect_timeout': 10.0},
                {'tello_ip': '192.168.43.175'},
                {'tf_base': 'map'},
                {'tf_drone': 'drone'}
            ],
            remappings=[
                ('/image_raw', '/camera')
            ],
            respawn=True
        ),

        Node(
            
            package='my_tello',
            executable='create_tello',
            output='screen',
            namespace='/',
            name='tello2',
            parameters=[
                {'connect_timeout': 10.0},
                {'tello_ip': '192.168.43.6'},
                {'tf_base': 'map'},
                {'tf_drone': 'drone'}
            ],
            remappings=[
                ('/image_raw', '/camera')
            ],
            respawn=True
        )
    ])


    