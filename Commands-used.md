Run the project using tcommands
colcon build
source install/setup.bash
ros2 launch my_robot_description arm_display.launch.py 


 


Open new terminal and run one of this command.
For controlling the arm using position, velocity and time
C0ommand :::::: run in terminal 

ros2 action send_goal /arm_trajectory_controller/follow_joint_trajectory control_msgs/action/FollowJointTrajectory "{ 
  trajectory: {
    joint_names: ['base_to_link_1_joint', 'link_1_to_link_2_joint'],
    points: [
      { positions: [1.0, -0.5], velocities: [0.0, 0.0], time_from_start: { sec: 3, nanosec: 0 } },
      { positions: [0.0, 0.0], velocities: [0.0, 0.0], time_from_start: { sec: 6, nanosec: 0 } }
    ]                                           
  }     
}" --feedback






For controlling the arm using position, velocity, acceleration and time
C0ommand :::::: run in terminal 

ros2 action send_goal /arm_trajectory_controller/follow_joint_trajectory control_msgs/action/FollowJointTrajectory "{
  trajectory: {
    joint_names: ['base_to_link_1_joint', 'link_1_to_link_2_joint'],
    points: [
      { 
        positions: [1.0, -0.5], 
        velocities: [0.0, 0.0], 
        accelerations: [0.0, 0.0], 
        time_from_start: { sec: 3, nanosec: 0 } 
      },
      { 
        positions: [0.0, 0.0], 
        velocities: [0.0, 0.0], 
        accelerations: [0.0, 0.0], 
        time_from_start: { sec: 6, nanosec: 0 } 
      }
    ]
  }
}" --feedback
