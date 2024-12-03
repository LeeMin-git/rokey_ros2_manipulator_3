import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    use_sim_time=LaunchConfiguration('use_sim_time')
    pkg_path=os.path.join(get_package_share_directory('urdf_tutorial'))
    xacro_file = os.path.join(pkg_path,'urdf','robot_1.xacro')
    robot_descriprion = xacro.process_file(xacro_file)
    params = {'robot_desrcription': robot_descriprion.toxml(), 'use_sim_time':use_sim_time}

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use sim time'),
        Node(
            packge = 'robot_state_publisher',
            excutable='robot_state_publisher',
            output='screen',
            parameters=[params])
    ])