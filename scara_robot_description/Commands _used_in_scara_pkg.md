
## For creating the package

cd ~/ros2_wsv1/src

ros2 pkg create scara_robot_description --build-type ament_cmake --dependencies xacro robot_state_publisher gazebo_ros gazebo_ros2_control

cd scara_robot_description

mkdir -p urdf config launch

---
## Add this before the end and remove/comment the second if condition.
Copy asset folders into the ROS 2 install share directory

install(
  DIRECTORY urdf config launch
  DESTINATION share/${PROJECT_NAME}
)


---
## After setup the files build the package
cd ~/ros2_wsv1

colcon build     or     colcon build --packages-select scara_robot_description

source install/setup.bash
