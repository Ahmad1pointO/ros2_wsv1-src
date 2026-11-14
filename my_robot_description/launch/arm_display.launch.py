# ============================== NAME LEGEND ==============================
# [FIXED] = exact name of installed software or a ROS standard. Do NOT change.
# [MATCH] = must be spelled exactly the same in every place listed.
# [FREE]  = a label you chose. Rename it freely (then update the [MATCH] places).
#
# Python variable names (package_dir, robot_desc, spawn_robot_gazebo, ...) are all
# [FREE]. They only need to match where the same variable is used later in this file.
# =========================================================================
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
    # 'my_robot_description'  [MATCH]  with <name> in package.xml and project() in CMakeLists.txt.
    # Gives: ~/ros2_wsv1/install/my_robot_description/share/my_robot_description
    package_dir = get_package_share_directory('my_robot_description')
    # 'urdf', 'robotic_arm.urdf.xacro'  [MATCH]  real folder + file name. The urdf folder
    # must be in install(DIRECTORY ...) in CMakeLists.txt.
    urdf_file_path = os.path.join(package_dir, 'urdf', 'robotic_arm.urdf.xacro')
    # 'config', 'arm_controllers.yaml'  [MATCH]  real folder + file name (also written in the xacro)
    yaml_file = os.path.join(package_dir, 'config', 'arm_controllers.yaml')   # NEW


    # xacro turns the .xacro into plain URDF text and resolves the find command in it.
    robot_desc = xacro.process_file(urdf_file_path).toxml()
    # Remove XML comments. They can break how the URDF is passed to the Gazebo plugin.
    robot_desc = re.sub(r'<!--.*?-->', '', robot_desc, flags=re.DOTALL)
    # NOTE: this line most likely does nothing. xacro (above) already replaced the find
    # command with the real path, so there is nothing left to replace. Harmless.
    robot_desc = robot_desc.replace('$(find my_robot_description)/config/arm_controllers.yaml', yaml_file)

    robot_state_publisher_node = Node(
        package='robot_state_publisher',      # [FIXED]  installed ROS package
        executable='robot_state_publisher',   # [FIXED]  program inside that package
        name='robot_state_publisher',         # [FREE]   node name you see in `ros2 node list`
        output='screen',
        # 'robot_description'  [FIXED]  parameter name robot_state_publisher expects.
        #   It then publishes the URDF on the /robot_description topic (used by the spawner below).
        # 'use_sim_time'  [FIXED]  standard ROS param: use Gazebo's clock instead of the PC clock.
        parameters=[{'robot_description': robot_desc, 'use_sim_time': True}]
    )

    # (Not used in the final LaunchDescription. Only for RViz testing without Gazebo.)
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',      # [FIXED]
        executable='joint_state_publisher_gui',   # [FIXED]
        name='joint_state_publisher_gui',         # [FREE]
        output='screen'
    )

    # (Not used in the final LaunchDescription.)
    rviz_node = Node(
        package='rviz2',      # [FIXED]
        executable='rviz2',   # [FIXED]
        name='rviz2',         # [FREE]
        output='screen'
    )

    # 'gazebo_ros', 'launch', 'gazebo.launch.py'  [FIXED]  launch file shipped with gazebo_ros
    gazebo_ros_dir = get_package_share_directory('gazebo_ros')
    launch_gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_dir, 'launch', 'gazebo.launch.py')
        )
    )


    spawn_robot_gazebo = Node(
    package='gazebo_ros',          # [FIXED]
    executable='spawn_entity.py',  # [FIXED]  script that puts a robot into Gazebo
    arguments=[
        # '-topic', '-entity', '-z'  [FIXED]  option names of spawn_entity.py
        # 'robot_description'  [MATCH]  topic published by robot_state_publisher (above)
        '-topic', 'robot_description',
        # 'my_robotic_arm'  [FREE]  the model's name inside Gazebo (Gazebo's model list)
        '-entity', 'my_robotic_arm',
        '-z', '0.0',
    ],
    output='screen'
    )




    # 'ros2', 'control', 'load_controller', '--set-state', 'active'  [FIXED]  ros2 CLI command
    # 'joint_state_broadcaster'  [MATCH]  with the controller name in config/arm_controllers.yaml
    load_joint_satate_broacaster = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'joint_state_broadcaster'],
        output='screen'
    )

    # 'arm_position_controller'  [MATCH]  with the controller name in config/arm_controllers.yaml
    # (both under controller_manager: and the top-level arm_position_controller: block)
    load_arm_position_controller= ExecuteProcess(
        # cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'arm_position_controller'],
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'arm_trajectory_controller'],
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

    # Wait until spawn_entity.py finishes (robot is in Gazebo, so the plugin and
    # controller_manager exist), THEN load the controllers.
    load_controlelrs_after_spawn = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_robot_gazebo,
            on_exit=[load_joint_satate_broacaster, load_arm_position_controller],
        )
    )

    # Start order: robot_state_publisher => Gazebo => (5 s later) spawn robot => load controllers
    return LaunchDescription([
        robot_state_publisher_node,
        launch_gazebo_server,
        TimerAction(period=5.0, actions=[spawn_robot_gazebo]),
        load_controlelrs_after_spawn,
    ])
