import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    ld = LaunchDescription()

    ROBOT_MODEL = 'robot_a'
    NAMESPACE = 'test'
    X_POS='-1.5'
    Y_POS='-0.5'

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    declare_use_sim_time = DeclareLaunchArgument(
        name='use_sim_time', default_value=use_sim_time, description='Use simulator time'
    )
    package_dir = get_package_share_directory('description')

    world = os.path.join(package_dir,'worlds', 'multi_robot_world.world')

    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world}.items(),
    )

    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gzclient.launch.py')
        ),
    )
    xacro_file = os.path.join(package_dir,'urdf','robot_a.xacro')
    robot_descriprion = xacro.process_file(xacro_file)
    params = {'robot_description': robot_descriprion.toxml(), 'use_sim_time':use_sim_time,'publish_frequency': 10.0 }
    robot_publisher = Node(
            package='robot_state_publisher',
            # namespace= NAMESPACE,
            executable='robot_state_publisher',
            output='screen',
            parameters=[params],
        )
    spawn_robot = Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=[
                '-file', os.path.join(package_dir,'models', ROBOT_MODEL, 'robot_a.sdf'),
                '-entity', ROBOT_MODEL,
                # '-robot_namespace', NAMESPACE,
                '-x', X_POS, '-y', Y_POS,
                '-z', '0.36', '-Y', '0.0',
                '-unpause',
            ],
            output='screen',
        )
    ld.add_action(declare_use_sim_time)
    ld.add_action(gzserver_cmd)
    ld.add_action(gzclient_cmd)
    ld.add_action(robot_publisher)
    # ld.add_action(spawn_robot)

    return ld