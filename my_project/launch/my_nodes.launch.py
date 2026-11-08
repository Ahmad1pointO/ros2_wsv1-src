from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    # 1. Define Node A (The server / Publisher )
    node_a = Node(
        package= 'my_project',
        executable= 'node_a',
        name= 'Coorduinator_node',
        output = 'screen'
    )

    # 2, Define Node B (The Client / Subscriber)
    # node_b = Node(
    #     package= 'my_project',
    #     executable= 'node_b',
    #     name= 'worker_node',
    #     output= 'screen'
    # )

    return LaunchDescription([
        node_a, 
        # node_b
        ])

