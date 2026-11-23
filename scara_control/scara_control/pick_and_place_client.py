import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from builtin_interfaces.msg import Duration

class ScaraActionClient(Node):
    def __init__(self):
        # Initialize the parent Node Class of ROS with our node name 
        super().__init__('scara_action_client')

        # Create the ActionClient and bind it to self so all methods canaccess it
        self._action_client = ActionClient(
            self,
            FollowJointTrajectory,
            '/scara_trajectory_controller/follow_joint_trajectory'
        )

    def send_pick_and_place_goal(self):
        self.get_logger().info('Waiting For the scara_trajectory_cntroller action server....')
        self._action_client.wait_for_server()

        # 1. Create a goal message container
        goal_msg = FollowJointTrajectory.Goal()
        goal_msg.trajectory.joint_names = ['joint_1', 'joint_2', 'joint_3', 'joint_4']

        # 2. Deine Waypoint 1: Swing over pick station (t = 3.0s)
        point_1 = JointTrajectoryPoint()
        point_1.positions = [0.8, -1.2, 0.0, 1.57]
        point_1.velocities = [0.0, 0.0, 0.0, 0.0]
        point_1.accelerations = [0.0, 0.0, 0.0, 0.0]
        point_1.time_from_start = Duration(sec=3, nanosec=0)

        # 3. Define Waypoint 2: Lower prismatic quill 12cm to pick part (t = 5.0s)
        point_2 = JointTrajectoryPoint()
        point_2.positions = [0.8, -1.2, -0.12, 1.57]
        point_2.velocities = [0.0, 0.0, 0.0, 0.0]
        point_2.accelerations = [0.0, 0.0, 0.0, 0.0]
        point_2.time_from_start = Duration(sec=5, nanosec=0)    

        # 4. Define Waypoint 3: Retract quill & return to home pose (t = 8.0s)
        point_3 = JointTrajectoryPoint()
        point_3.positions = [0.0, 0.0, 0.0, 0.0]
        point_3.velocities = [0.0, 0.0, 0.0, 0.0]
        point_3.accelerations = [0.0, 0.0, 0.0, 0.0]
        point_3.time_from_start = Duration(sec=8, nanosec=0)

        # Attach all the waypoints to the trajectory
        goal_msg.trajectory.points = [point_1, point_2, point_3]

        self.get_logger().info('Sending 3-waypoint quintic pick-and-place trajectory...')

        # 5. Send the goal asynchroneusly and register our feedback callback
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback = self.feedback_callback
        )

        #Register callback for When th server accepts /rejects he goal
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Trajectory Goal was Rejected by Controller!')
            rclpy.shutdown()
            return
        
        self.get_logger().info('Trajectory Goal Accepted by Controller!, Executing Trajectory spline...')
        # Request the final execution result asynchronously
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)
    
    def feedback_callback(self, feedback_msg):
        # Extract Live tracking erros fro all four joints
        errors = feedback_msg.feedback.error.positions
        formatted_errors = [ round(e, 4) for e in errors]
        self.get_logger().info(f'Live Joint Position Errors[j1, j2, j3, j4]: {formatted_errors}')

    def get_result_callback(self, future):
        result = future.result().result
        if result.error_code == 0:
            self.get_logger().info('Trajectory Execution Complete: SUCCESS, Pick and Place cycle complete!')
        else:
            self.get_logger().warn(f'Trajectory Finished with error Code: {result.error_code}')
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    action_client = ScaraActionClient()
    action_client.send_pick_and_place_goal()
    rclpy.spin(action_client)


if __name__ == '__main__':
    main()

