
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

ros2 launch scara_robot_description scara_gazebo.launch.py 








```bash
ros2 action send_goal /scara_trajectory_controller/follow_joint_trajectory control_msgs/action/FollowJointTrajectory "{
  trajectory: {
    joint_names: ['joint_1', 'joint_2', 'joint_3', 'joint_4'],
    points: [
      { positions: [0.8, -1.2, 0.0, 1.57],   velocities: [0.0, 0.0, 0.0, 0.0], accelerations: [0.0, 0.0, 0.0, 0.0], time_from_start: { sec: 3, nanosec: 0 } },
      { positions: [0.8, -1.2, -0.12, 1.57], velocities: [0.0, 0.0, 0.0, 0.0], accelerations: [0.0, 0.0, 0.0, 0.0], time_from_start: { sec: 5, nanosec: 0 } },
      { positions: [0.0, 0.0, 0.0, 0.0],     velocities: [0.0, 0.0, 0.0, 0.0], accelerations: [0.0, 0.0, 0.0, 0.0], time_from_start: { sec: 8, nanosec: 0 } }
    ]
  }
}" --feedback
```