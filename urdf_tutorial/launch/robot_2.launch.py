import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, Shutdown
from launch_ros.actions import Node
import xacro
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution, Command, LaunchConfiguration

def generate_launch_description():
    use_sim_time=LaunchConfiguration('use_sim_time')

    pkg_path=os.path.join(get_package_share_directory('description'))
    xacro_file = os.path.join(pkg_path,'urdf','robot_2.xacro')
    robot_descriprion = xacro.process_file(xacro_file)
    params = {'ignore_timestamp': False,'robot_description': robot_descriprion.toxml(), 'use_sim_time':use_sim_time}
    rviz_config_file = PathJoinSubstitution([
            FindPackageShare('description'),
            'rviz',
            'robot.rviz'
        # 안해도 오류는 없는데, 저장된 설정을 가져옵니다. 이런 느낌이다.
        ])
    
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
            on_exit=Shutdown()),
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
