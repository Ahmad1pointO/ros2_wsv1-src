import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
import xacro
import re

def generate_launch_description():
    package_dir = get_package_share_directory('my_robot_description')
    urdf_file_path = os.path.join(package_dir, 'urdf', 'robotic_arm.urdf.xacro')
    yaml_file = os.path.join(package_dir, 'config', 'arm_controllers.yaml')   # NEW


    robot_desc = xacro.process_file(urdf_file_path).toxml()
    robot_desc = re.sub(r'<!--.*?-->', '', robot_desc, flags=re.DOTALL)
    robot_desc = robot_desc.replace('$(find my_robot_description)/config/arm_controllers.yaml', yaml_file)

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc, 'use_sim_time': True}]
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen'
    )

    gazebo_ros_dir = get_package_share_directory('gazebo_ros')
    launch_gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_dir, 'launch', 'gazebo.launch.py')
        )
    )


    spawn_robot_gazebo = Node(
    package='gazebo_ros',
    executable='spawn_entity.py',
    arguments=[
        '-topic', 'robot_description',
        '-entity', 'my_robotic_arm',
        '-z', '0.0',
    ],
    output='screen'
    )




    load_joint_satate_broacaster = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'joint_state_broadcaster'],
        output='screen'
    ) 

    load_arm_position_controller= ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'arm_position_controller'],
        output='screen'
    )




    # return LaunchDescription([
    #     robot_state_publisher_node,
    #     # joint_state_publisher_gui_node,
    #     # rviz_node,
    #     launch_gazebo_server,
    #     # spawn_robot_gazebo,
    #     TimerAction(period=5.0, actions=[spawn_robot_gazebo]),
    #     load_joint_satate_broacaster,
    #     load_arm_position_controller

    # ])

    load_controlelrs_after_spawn = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_robot_gazebo,
            on_exit=[load_joint_satate_broacaster, load_arm_position_controller],
        )
    )

    return LaunchDescription([
        robot_state_publisher_node,
        launch_gazebo_server,
        TimerAction(period=5.0, actions=[spawn_robot_gazebo]),
        load_controlelrs_after_spawn,
    ])