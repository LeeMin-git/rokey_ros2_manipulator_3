import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, Shutdown
from launch_ros.actions import Node

def generate_launch_description():
    use_sim_time=LaunchConfiguration('use_sim_time')

    pkg_path=os.path.join(get_package_share_directory('description'))
    xacro_file = os.path.join(pkg_path,'urdf','robot_b.xacro')
    robot_descriprion = xacro.process_file(xacro_file)
    params = {'ignore_timestamp': False,'robot_description': robot_descriprion.toxml(), 'use_sim_time':use_sim_time}
    rviz_config_file=os.path.join(pkg_path,'rviz','robot.rviz')
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time'),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config_file],
            #on_exit=Shutdown()
            ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[params]),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher',
            output='screen')
    ])
