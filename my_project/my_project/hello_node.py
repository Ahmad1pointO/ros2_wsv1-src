import rclpy
from rclpy.node import Node

class MyFirstNode(Node):
    def __init__(self):
        super().__init__('hello_node')
        self.get_logger().info('Hello from your first ROS 2 Project!')

def main(args=None):
    rclpy.init(args=args)
    node = MyFirstNode()
    rclpy.spin(node) # Keeps the node alive
    rclpy.shutdown()

if __name__ == '__main__':
    main()
