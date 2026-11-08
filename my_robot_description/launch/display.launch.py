# import os
# from ament_index_python.packages import get_package_share_directory
# from launch import LaunchDescription
# from launch_ros.actions import Node

# def generate_launch_description():
#     # 1. Locate your description package folder
#     package_dir = get_package_share_directory('my_robot_description')
    
#     # 2. Define the path straight to your .urdf file asset
#     urdf_file_path = os.path.join(package_dir, 'urdf', 'my_robot.urdf')
    
#     # 3. Read the URDF file contents into memory safely
#     with open(urdf_file_path, 'r') as infp:
#         robot_desc = infp.read()

#     # 4. Configure the background publisher engine node
#     robot_state_publisher_node = Node(
#         package='robot_state_publisher',
#         executable='robot_state_publisher',
#         name='robot_state_publisher',
#         output='screen',
#         parameters=[{'robot_description': robot_desc}] # Injects the file cleanly
#     )

#     # 5. Configure the RViz visual interface tool node
#     rviz_node = Node(
#         package='rviz2',
#         executable='rviz2',
#         name='rviz2',
#         output='screen'
#     )

#     return LaunchDescription([
#         robot_state_publisher_node,
#         rviz_node
#     ])



import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Locate your description package folder
    package_dir = get_package_share_directory('my_robot_description')
    
    # 2. Define the path straight to your .urdf file asset
    urdf_file_path = os.path.join(package_dir, 'urdf', 'my_robot.urdf')
    
    # 3. Read the URDF file contents into memory safely
    with open(urdf_file_path, 'r') as infp:
        robot_desc = infp.read()

    # 4. Configure the background publisher engine node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}]
    )

    # 5. NEW: Add the Joint State Publisher GUI node
    # This node calculates the joint transforms and solves the wheel centering bug!
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    # 6. Configure the RViz visual interface tool node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen'
    )

    

    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_gui_node, # Now tracking joint offsets
        rviz_node
    ])
