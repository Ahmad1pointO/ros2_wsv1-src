import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
import xacro

def generate_launch_description():
    package_dir = get_package_share_directory('my_robot_description')
    
    urdf_file_path = os.path.join(package_dir, 'urdf', 'robotic_arm.urdf.xacro')
    robot_desc = xacro.process_file(urdf_file_path).toxml()

        # Target our brand-new robotic_arm.urdf file instead!
    # urdf_file_path = os.path.join(package_dir, 'urdf', 'robotic_arm1.urdf')
    
    # with open(urdf_file_path, 'r') as infp:
    #     robot_desc = infp.read()

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}]
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

    # # spawn_robot_gazebo = Node(
    # #     package='gazebo_ros',
    # #     executable = 'spawn_entity.py',
    # #     arguments=[
    # #         '-topic', 'robot_description',
    # #         '-entity', 'my_robotic_arm',
    # #         '-z', '0.1',
    # #     ],
    # #     output = 'screen'
    # # )

    spawn_robot_gazebo = Node(
    package='gazebo_ros',
    executable='spawn_entity.py',
    arguments=[
        '-topic', 'robot_description',
        '-entity', 'my_robotic_arm',
        '-z', '0.1',
    ],
    output='screen'
    )


    # # # urdf_file = os.path.join(package_dir, 'urdf', 'robotic_arm1.urdf')
    # spawn_robot_gazebo = Node(
    #     package='gazebo_ros',
    #     executable='spawn_entity.py',
    #     arguments=[
    #         '-file', urdf_file,
    #         '-entity', 'my_robotic_arm',
    #         '-z', '0.0',
    #     ],
    #     output='screen'
    # )


    # load_joint_satate_broacaster = ExecuteProcess(
    #     cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'joint_state_broadcaster'],
    #     output='screen'
    # ) 

    # load_arm_position_controller= ExecuteProcess(
    #     cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'arm_position_controller'],
    #     output='screen'
    # )




    return LaunchDescription([
        robot_state_publisher_node,
        # joint_state_publisher_gui_node,
        # rviz_node,
        launch_gazebo_server,
        spawn_robot_gazebo,
        # TimerAction(period=5.0, actions=[spawn_robot_gazebo]),
        # load_joint_satate_broacaster,
        # load_arm_position_controller

    ])





# import os
# from ament_index_python.packages import get_package_share_directory
# from launch import LaunchDescription
# from launch.actions import IncludeLaunchDescription, RegisterEventHandler, TimerAction
# from launch.event_handlers import OnProcessExit
# from launch.launch_description_sources import PythonLaunchDescriptionSource
# from launch_ros.actions import Node


# def generate_launch_description():
#     package_dir = get_package_share_directory('my_robot_description')
#     gazebo_ros_dir = get_package_share_directory('gazebo_ros')

#     urdf_file = os.path.join(package_dir, 'urdf', 'robotic_arm1.urdf')
#     yaml_file = os.path.join(package_dir, 'config', 'arm_controllers.yaml')

#     # Read URDF and replace the $(find ...) placeholder with the real path
#     with open(urdf_file, 'r') as f:
#         robot_desc = f.read()
#     robot_desc = robot_desc.replace(
#         '$(find my_robot_description)/config/arm_controllers.yaml', yaml_file)

#     robot_state_publisher = Node(
#         package='robot_state_publisher',
#         executable='robot_state_publisher',
#         output='screen',
#         parameters=[{'robot_description': robot_desc,
#                      'use_sim_time': True}]
#     )

#     gazebo = IncludeLaunchDescription(
#         PythonLaunchDescriptionSource(
#             os.path.join(gazebo_ros_dir, 'launch', 'gazebo.launch.py')
#         )
#     )

#     spawn_robot = Node(
#         package='gazebo_ros',
#         executable='spawn_entity.py',
#         arguments=['-topic', 'robot_description',
#                    '-entity', 'my_robotic_arm',
#                    '-z', '0.5'],
#         output='screen'
#     )

#     joint_state_broadcaster = Node(
#         package='controller_manager',
#         executable='spawner',
#         arguments=['joint_state_broadcaster',
#                    '--controller-manager', '/controller_manager'],
#         output='screen'
#     )

#     arm_position_controller = Node(
#         package='controller_manager',
#         executable='spawner',
#         arguments=['arm_position_controller',
#                    '--controller-manager', '/controller_manager'],
#         output='screen'
#     )

#     # Load controllers only after the robot is spawned
#     load_jsb_after_spawn = RegisterEventHandler(
#         OnProcessExit(target_action=spawn_robot,
#                       on_exit=[joint_state_broadcaster])
#     )
#     load_arm_after_jsb = RegisterEventHandler(
#         OnProcessExit(target_action=joint_state_broadcaster,
#                       on_exit=[arm_position_controller])
#     )

#     return LaunchDescription([
#         robot_state_publisher,
#         gazebo,
#         TimerAction(period=2.0, actions=[spawn_robot]),
#     #     load_jsb_after_spawn,
#     #     load_arm_after_jsb,
#     ])