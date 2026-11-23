import os 
import re
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node




def generate_launch_description():
    package_dir = get_package_share_directory('scara_robot_description')
    urdf_file_path = os.path.join(package_dir, 'urdf', 'abb_scara.urdf.xacro')
    yaml_file_path = os.path.join(package_dir, 'config', 'scara_controllers.yaml')

    # compile the xacro file to XML, Strip comments, and resolve the YAML Path string
    robot_desc = xacro.process_file(urdf_file_path).toxml()
    robot_desc = re.sub(r'<!--.*?-->', '', robot_desc, flags=re.DOTALL)
    robot_desc = robot_desc.replace('$(find scara_robot_description)/config/scara_controllers.yaml', yaml_file_path)

    # 1. Robot state publisher node
    robot_state_publisher_node = Node(
        package = 'robot_state_publisher',
        executable = 'robot_state_publisher',
        name = 'robot_state_publisher',
        output = 'screen',
        parameters = [{'robot_description': robot_desc, 'use_sim_time': True}]
    )

    joint_state_publisher_node = Node(
            package = 'joint_state_publisher',
            executable = 'joint_state_publisher',
            name = 'joint_state_publisher',
            output = 'screen',
            parameters = [{'use_sim_time': True}]
        )
    rviz_node = Node(
        package = 'rviz2',
        executable = 'rviz2',
        name = 'rviz2',
        output = 'screen',
    )
    

    # 2. Gazebo Server & Client launch files
    gazebo_ros_dir = get_package_share_directory('gazebo_ros')
    launch_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_dir, 'launch', 'gazebo.launch.py')
        )
    )

    spawn_scara_node = Node(
        package = 'gazebo_ros',
        executable = 'spawn_entity.py',
        arguments = ['-topic', 'robot_description', 
                     '-entity', 'scara_robot'],
        output = 'screen'
    )
    # 4. Controllers Loader
    load_joint_state_broadcaster = ExecuteProcess(
        cmd = ['ros2', 'control', 'load_controller', '--set-state', 'active', 'joint_state_broadcaster'],
        output = 'screen'
    )

    laod_scara_trajectory_controller = ExecuteProcess(
        cmd = ['ros2', 'control', 'load_controller', '--set-state', 'active', 'scara_trajectory_controller'],
        output = 'screen'
    )   

  
    laod_controllers_after_spawn = RegisterEventHandler(
        event_handler = OnProcessExit(
            target_action = spawn_scara_node,
            on_exit = [load_joint_state_broadcaster, 
                        laod_scara_trajectory_controller]
        )
    )

    return LaunchDescription([
        robot_state_publisher_node,
        # joint_state_publisher_node,
        rviz_node,
        launch_gazebo,
        TimerAction(period = 3.0, actions=[spawn_scara_node]),
        laod_controllers_after_spawn
        
    ])