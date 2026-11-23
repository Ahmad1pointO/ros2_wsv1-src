## Making Sacra Robot Control 
cd ~/ros2_wsv1/src
ros2 pkg create scara_control --build-type ament_python --dependencies rclpy control_msgs trajectory_msgs builtin_interfaces
