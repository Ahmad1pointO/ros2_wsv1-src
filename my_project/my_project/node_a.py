# # # # # # # # import rclpy
# # # # # # # # from rclpy.node import Node
# # # # # # # # from std_msgs.msg import String  # Import the standard string message type

# # # # # # # # class NodeA(Node):
# # # # # # # #     def __init__(self):
# # # # # # # #         super().__init__('node_a')
# # # # # # # #         # Create a publisher that sends String messages on a topic named '/status'
# # # # # # # #         # The '10' is the queue size (buffer)
# # # # # # # #         self.publisher_ = self.create_publisher(String, 'status', 10)
        
# # # # # # # #         # Create a timer that triggers the 'timer_callback' function every 1.0 seconds
# # # # # # # #         self.timer = self.create_timer(1.0, self.timer_callback)
# # # # # # # #         self.get_logger().info('Node A (Publisher) has started!')

# # # # # # # #     def timer_callback(self):
# # # # # # # #         msg = String()
# # # # # # # #         msg.data = 'System Status: OK'
# # # # # # # #         self.publisher_.publish(msg)  # Send the message over the network
# # # # # # # #         self.get_logger().info(f'Published: "{msg.data}"')

# # # # # # # # def main(args=None):
# # # # # # # #     rclpy.init(args=args)
# # # # # # # #     node = NodeA()
# # # # # # # #     rclpy.spin(node)
# # # # # # # #     rclpy.shutdown()

# # # # # # # # if __name__ == '__main__':
# # # # # # # #     main()





# # # # # # # """ Making a Topic that is sending the string to the Subscriber from Publisher"""
# # # # # # # import rclpy
# # # # # # # from std_msgs.msg import String
# # # # # # # # from rclpy.node import Node


# # # # # # # def timer_callback(publisher, node):
# # # # # # #     msg = String()
# # # # # # #     msg.data =  'System Status Okay'
# # # # # # #     publisher.publish(msg)
# # # # # # #     node.get_logger().info(f'Published: "{msg.data}"')

# # # # # # # def main(args = None):
# # # # # # #     rclpy.init(args = args)
# # # # # # #     node = rclpy.create_node('node_a')
# # # # # # #     publisher = node.create_publisher(String, 'status', 10)
# # # # # # #     node.create_timer(1.0, lambda: timer_callback(publisher, node))
# # # # # # #     node.get_logger().info('Node A (Functional Publisher) has Started')
# # # # # # #     rclpy.spin(node)
# # # # # # #     rclpy.shutdown()


# # # # # # # if __name__ == '__main__':
# # # # # # #     main()



# # # # # # # """ Making a Topic that is sending the data(integers) from Publisher to Subscriber"""
# # # # # # # import rclpy
# # # # # # # from std_msgs.msg import Int32
# # # # # # # counts = 20

# # # # # # # def timer_callback(publisher, node, counter_list, counts):
# # # # # # #     if counter_list[0] >= counts:
# # # # # # #         node.get_logger().info(f'Reached "{counts}!" Stopping the Publisher node...')
# # # # # # #         node.destroy_node()
# # # # # # #         rclpy.shutdown()
# # # # # # #         return

# # # # # # #     msg = Int32()
# # # # # # #     msg.data = counter_list[0]
# # # # # # #     publisher.publish(msg)
# # # # # # #     node.get_logger().info(f'Pubished: {msg.data}')
# # # # # # #     counter_list[0] +=1

# # # # # # # def main(args = None):
# # # # # # #     rclpy.init(args= args)
# # # # # # #     node = rclpy.create_node('node_a')

# # # # # # #     counter_list = [0]
# # # # # # #     publisher = node.create_publisher(Int32, 'Data', 10)
# # # # # # #     node.create_timer(1.0, lambda: timer_callback(publisher, node, counter_list, counts))

# # # # # # #     node.get_logger().info('Node A is (Functional Counter) has started!')
# # # # # # #     try:
# # # # # # #         rclpy.spin(node)
# # # # # # #     except(KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
# # # # # # #         pass

# # # # # # # if __name__ == '__main__':
# # # # # # #     main()



# # # # # # """ Making a topic that is Publishing data when ever the interrupt is happening on the node a"""
# # # # # # import rclpy 
# # # # # # from std_msgs.msg import Int32
# # # # # # import threading
# # # # # # import time

# # # # # # counter = 0
# # # # # # counts = 100

# # # # # # def hardware_sensor_loop(publisher, node, counts):
# # # # # #     global counter

# # # # # #     while rclpy.ok():
# # # # # #         if counter > counts:
# # # # # #             node.get_logger().info(f'Reached {counts}! Stoping the publisher node ....')
# # # # # #             node.destroy_node()
# # # # # #             rclpy.shutdown()
# # # # # #             break

# # # # # #         time.sleep(1.0)

# # # # # #         msg = Int32()
# # # # # #         msg.data = counter
# # # # # #         publisher.publish(msg)
# # # # # #         node.get_logger().info(f'[EVENT-DRIVEN] Published: {msg.data}')

# # # # # #         counter += 1


# # # # # # def main(args=None):
# # # # # #     global counts
# # # # # #     rclpy.init(args=args)
# # # # # #     node = rclpy.create_node('node_a')
# # # # # #     publisher  = node.create_publisher(Int32,'Data', 10)
# # # # # #     node.get_logger().info('Node A (Event-Driven Sensor) has started!')

# # # # # #     sensor_thread = threading.Thread(target=hardware_sensor_loop, args= (publisher, node, counts))
# # # # # #     sensor_thread.start()

# # # # # #     try:
# # # # # #         rclpy.spin(node)
# # # # # #     except(KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
# # # # # #         pass


# # # # # # if __name__ == '__main__':
# # # # # #     main()



# # # # # # # import rclpy
# # # # # # # from std_msgs.msg import Int32
# # # # # # # import threading
# # # # # # # import time

# # # # # # # counter = 0

# # # # # # # # This function acts like a hardware interrupt service routine (ISR)
# # # # # # # def hardware_sensor_loop(publisher, node):
# # # # # # #     global counter
    
# # # # # # #     while rclpy.ok():
# # # # # # #         if counter >= 10:
# # # # # # #             node.get_logger().info('Reached 10! Stopping the publisher node...')
# # # # # # #             node.destroy_node()
# # # # # # #             rclpy.shutdown()
# # # # # # #             break

# # # # # # #         # SIMULATING AN INTERRUPT: Imagine the hardware takes random 
# # # # # # #         # amounts of time to process a sensor reading (e.g., between 0.5 to 1.5 seconds)
# # # # # # #         time.sleep(1.0) 

# # # # # # #         # The moment data "arrives" from hardware, we instantly publish it!
# # # # # # #         msg = Int32()
# # # # # # #         msg.data = counter
# # # # # # #         publisher.publish(msg)
# # # # # # #         node.get_logger().info(f'[EVENT-DRIVEN] Published: {msg.data}')
        
# # # # # # #         counter += 1

# # # # # # # def main(args=None):
# # # # # # #     rclpy.init(args=args)
# # # # # # #     node = rclpy.create_node('node_a')
    
# # # # # # #     publisher = node.create_publisher(Int32, 'status', 10)
# # # # # # #     node.get_logger().info('Node A (Event-Driven Sensor) has started!')

# # # # # # #     # Start a background thread to handle the incoming sensor events
# # # # # # #     # This leaves the main thread free to handle ROS 2 system loops
# # # # # # #     sensor_thread = threading.Thread(target=hardware_sensor_loop, args=(publisher, node))
# # # # # # #     sensor_thread.start()
    
# # # # # # #     try:
# # # # # # #         rclpy.spin(node)
# # # # # # #     except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
# # # # # # #         pass

# # # # # # # if __name__ == '__main__':
# # # # # # #     main()







# # # # # """ Implementing the Service 
# # # # # /ping_worker: Node A calls this service, and Node B hosts the server.
# # # # # /ping_coordinator: Node B calls this service, and Node A hosts the server.
# # # # # """

# # # # # # import rclpy
# # # # # # from example_interfaces.srv import Trigger

# # # # # # """The Service server Logic ;;; Node_a revices the request and response on this"""
# # # # # # def cordinator_service_callback(request, response):
# # # # # #     response.success = True
# # # # # #     response.message = 'Pong from Coordinatore!'
# # # # # #     return response


# # # # # # """ The Service Client Logic ::: Node_a ask the Node_b and got reply"""
# # # # # # def call_worker_service(node, Client):
# # # # # #     while not Client.wait_for_services(timeout_src = 0.1):
# # # # # #         node.get_logger().info('wait for worker service to become available ...')
# # # # # #         req = Trigger.Request()

# # # # # #         node.get_logger().info('Sending Request to the worker:"ping"')
# # # # # #         future  = Client.call_async(req)


# # # # # #     """ Look for teh answer without response"""
# # # # # #     def response_recieved_callback(completed_future):
# # # # # #         try:
# # # # # #             result = completed_future.result()
# # # # # #             node.get_logger().error(f'Response recieved from worker: "{result.message}"')
# # # # # #         except Exception as e:
# # # # # #             node.get_logger().error(f'service calld failed: {e}')

# # # # # #     future.add_one_callback(response_recieved_callback)

# # # # # # def main(args = None):
# # # # # #     rclpy.init(args=args)
# # # # # #     node = rclpy.create_node('node_a')

# # # # # #     server = node.create_service(Trigger, 'Ping_coordinatore', coordinator_service_callback)
# # # # # #     client = node.create_client(Trigger,'ping_worker')
# # # # # #     node.get_logger().info(3.0, lambda: call_worker_service(node. client))

# # # # # #     try:
# # # # # #         rclpy.spin(node)
# # # # # #     except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
# # # # # #         pass
# # # # # #     finally:
# # # # # #         node.destroy_node()
# # # # # #         node.shutdown()

# # # # # # if __name__ == '__main__':
# # # # # #     main()






# # # # # # import rclpy
# # # # # # from example_interfaces.srv import Trigger  # Standard Service type (empty request, string response)

# # # # # # # --- 1. THE SERVICE SERVER LOGIC (Node A receives a request and replies) ---
# # # # # # def coordinator_service_callback(request, response):
# # # # # #     # This runs when Node B calls '/ping_coordinator'
# # # # # #     response.success = True
# # # # # #     response.message = "Pong from Coordinator!"
# # # # # #     return response

# # # # # # # --- 2. THE SERVICE CLIENT LOGIC (Node A asks Node B for data) ---
# # # # # # def call_worker_service(node, client):
# # # # # #     # Wait for the worker service server to come online
# # # # # #     while not client.wait_for_service(timeout_sec=1.0):
# # # # # #         node.get_logger().info('Waiting for worker service to become available...')

# # # # # #     # Create an empty request package
# # # # # #     req = Trigger.Request()
    
# # # # # #     # Send the request asynchronously
# # # # # #     node.get_logger().info('Sending Request to Worker: "Ping"')
# # # # # #     future = client.call_async(req)
    
# # # # # #     # Look for the answer without freezing the node
# # # # # #     def response_received_callback(completed_future):
# # # # # #         try:
# # # # # #             result = completed_future.result()
# # # # # #             node.get_logger().info(f'Received Response from Worker: "{result.message}"')
# # # # # #         except Exception as e:
# # # # # #             node.get_logger().error(f'Service call failed: {e}')

# # # # # #     future.add_done_callback(response_received_callback)

# # # # # # def main(args=None):
# # # # # #     rclpy.init(args=args)
# # # # # #     node = rclpy.create_node('node_a')
    
# # # # # #     # Create the Server: Listen on '/ping_coordinator', route requests to the callback
# # # # # #     server = node.create_service(Trigger, 'ping_coordinator', coordinator_service_callback)
    
# # # # # #     # Create the Client: Targets the '/ping_worker' service hosted by Node B
# # # # # #     client = node.create_client(Trigger, 'ping_worker')
    
# # # # # #     node.get_logger().info('Node A (Coordinator Service Node) has started!')
    
# # # # # #     # Trigger a timer to call Node B's service 3 seconds after starting
# # # # # #     node.create_timer(3.0, lambda: call_worker_service(node, client))
    
# # # # # #     try:
# # # # # #         rclpy.spin(node)
# # # # # #     except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
# # # # # #         pass
# # # # # #     finally:
# # # # # #         node.destroy_node()
# # # # # #         rclpy.shutdown()

# # # # # # if __name__ == '__main__':
# # # # # #     main()



# # # # # import rclpy
# # # # # from example_interfaces.srv import Trigger

# # # # # node = None

# # # # # def server_callback(request, response):
# # # # #     response.success = True
# # # # #     response.message = 'Pong!'
# # # # #     node.get_logger().info('Answering the ')
# # # # #     return response

# # # # # def main(args = None):
# # # # #     global node
# # # # #     rclpy.init(args=args)
# # # # #     node = rclpy.create_node('minimal_server')
# # # # #     node.create_service(Trigger, 'ping_service', server_callback)
# # # # #     node.get_logger().info('Server is waiting for a request...')
# # # # #     rclpy.spin(node)
# # # # #     rclpy.shutdown()

# # # # # if __name__ == '__main__':
# # # # #     main()



# # # # import rclpy
# # # # from rclpy.action import ActionServer
# # # # from action_tutorials_interfaces.action import Fibonacci
# # # # import time

# # # # def execute_callback(goal_handle):
# # # #     # 1. Read the goal number sent by the client (e.g., 500)
# # # #     target_count = goal_handle.request.order
# # # #     goal_handle.get_logger().info(f'Executing goal: Counting up to {target_count}...')

# # # #     # Setup the feedback object and our counter loop variables
# # # #     feedback_msg = Fibonacci.Feedback()
# # # #     current_sequence = []

# # # #     # 2. Start the counting loop
# # # #     for i in range(1, target_count + 1):
# # # #         current_sequence.append(i)
        
# # # #         # Simulating an event happening every 1 second
# # # #         time.sleep(1.0)
        
# # # #         # 3. Publish the feedback back to the client live
# # # #         feedback_msg.sequence = current_sequence
# # # #         goal_handle.publish_feedback(feedback_msg)
# # # #         goal_handle.get_logger().info(f'Feedback sent: Count is {i}')

# # # #     # 4. Once finished, declare success and return the final result
# # # #     goal_handle.succeed()
# # # #     result = Fibonacci.Result()
# # # #     result.sequence = current_sequence
# # # #     return result

# # # # def main(args=None):
# # # #     rclpy.init(args=args)
# # # #     node = rclpy.create_node('minimal_action_server')

# # # #     # Create the Action Server
# # # #     # Arguments: (node_object, action_type, action_name, execution_callback_function)
# # # #     action_server = ActionServer(
# # # #         node,
# # # #         Fibonacci,
# # # #         'count_to_500',
# # # #         execute_callback
# # # #     )

# # # #     node.get_logger().info('Action Server is online and waiting for a goal...')

# # # #     try:
# # # #         rclpy.spin(node)
# # # #     except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
# # # #         pass
# # # #     finally:
# # # #         action_server.destroy()
# # # #         node.destroy_node()
# # # #         rclpy.shutdown()

# # # # if __name__ == '__main__':
# # # #     main()



# # # """ Understanding the parameters in Ros2 that could be configured at the runtime. """
# # # # import rclpy
# # # # import time 



# # # # def main():
# # # #     rclpy.init()
# # # #     node = rclpy.create_node('param_node')

# # # #     # 1. DECLARE THE PARAMETER: (parameter_name, default_value)
# # # #     node.declare_parameter('target_limit', 10)

# # # #     node.get_logger().info('Node started and waiting 10 seconds before configuration ...')
# # # #     time.sleep(10.0)



# # # #     current_limit = node.get_parameter('target_limit').value
# # # #     node.get_logger().info(f'the active trget limi is set to : {current_limit}')
# # # #     rclpy._shutdown()

# # # # if __name__ == '__main__':
# # # #     main()




# # # import rclpy

# # # def check_the_param_callback(node):
# # #     # pass
# # #     Current_set_limit = node.get_parameter('target_limit').value
# # #     node.get_logger().info(f'The Active target_limit is set to :{Current_set_limit}')

# # # def main():
# # #     rclpy.init()
# # #     node = rclpy.create_node('param_node')
# # #     node.declare_parameter('target_limit', 9)
# # #     current_limit = node.get_parameter('target_limit').value
# # #     node.get_logger().info(f'Current 11111 default value is {current_limit}')


# # #     node.create_timer(5.0, lambda: check_the_param_callback(node))

# # #     try:
# # #         rclpy.spin(node)
# # #     except(KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
# # #         pass
# # #     finally:
# # #         node.destroy_node()
# # #         rclpy.shutdown()

# # # if '__name__' == '__main__':
# # #     main()



# # """ Publishing data using our brand-new custom RobotStatus message """
# # import rclpy 
# # from my_robot_interfaces.msg import RobotStatus  # Import your custom compiled message type
# # import threading
# # import time

# # counter = 0
# # counts = 20

# # def hardware_sensor_loop(publisher, node, counts):
# #     global counter

# #     while rclpy.ok():
# #         if counter >= counts:
# #             node.get_logger().info(f'Reached {counts}! Stopping the publisher node ....')
# #             node.destroy_node()
# #             rclpy.shutdown()
# #             break

# #         time.sleep(1.0)

# #         # 1. Create an instance of your custom message
# #         msg = RobotStatus()
        
# #         # 2. Fill in the data slots exactly as you defined them in your .msg file
# #         msg.robot_id = 101
# #         msg.status_message = "Robot navigating smoothly"
# #         msg.battery_level = 98.5 - (counter * 0.5)  # Simulate battery draining over time

# #         # 3. Publish it over the network
# #         publisher.publish(msg)
# #         node.get_logger().info(
# #             f'[CUSTOM-MSG] Sent ID: {msg.robot_id} | Status: "{msg.status_message}" | Battery: {msg.battery_level}%'
# #         )

# #         counter += 1


# # def main(args=None):
# #     global counts
# #     rclpy.init(args=args)
# #     node = rclpy.create_node('node_a')
    
# #     # Update the topic type to use RobotStatus and changed topic name to 'robot_status_topic'
# #     publisher = node.create_publisher(RobotStatus, 'robot_status_topic', 10)
# #     node.get_logger().info('Node A (Custom Message Sensor Node) has started!')

# #     sensor_thread = threading.Thread(target=hardware_sensor_loop, args=(publisher, node, counts))
# #     sensor_thread.start()

# #     try:
# #         rclpy.spin(node)
# #     except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
# #         pass


# # if __name__ == '__main__':
# #     main()






# """ Custom Service Server implementation using SetLedColor.srv """
# import rclpy
# from my_robot_interfaces.srv import SetLedColor  # Import your custom service package

# # 1. Define what happens when a client calls the service
# def set_led_color_callback(request, response, node):
#     # 'request.color' accesses the string sent by the client
#     node.get_logger().info(f'Received request to change LED color to: "{request.color}"')

#     # Simulate basic robot hardware validation logic
#     valid_colors = ["red", "green", "blue", "yellow"]
    
#     if request.color.lower() in valid_colors:
#         response.success = True
#         response.message = f"Hardware confirmation: LED successfully changed to {request.color}."
#     else:
#         response.success = False
#         response.message = f"Hardware error: Color '{request.color}' is not supported by this robot."

#     # Return the completed response object back to the client
#     return response

# def main(args=None):
#     rclpy.init(args=args)
#     node = rclpy.create_node('led_service_server_node')

#     # 2. Create the service server channel
#     # Using a lambda to pass our local 'node' object into our external callback function
#     node.create_service(
#         SetLedColor,
#         'set_led_color',
#         lambda req, res: set_led_color_callback(req, res, node)
#     )

#     node.get_logger().info('Custom LED Service Server is now online and waiting for requests...')

#     try:
#         rclpy.spin(node)
#     except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
#         pass
#     finally:
#         node.destroy_node()
#         rclpy.shutdown()

# if __name__ == '__main__':
#     main()




""" Custom Action Server implementation using PatrolRoom.action """
import rclpy
from rclpy.action import ActionServer
from my_robot_interfaces.action import PatrolRoom  # Import your custom action type
import time

def execute_callback(goal_handle, node):
    # 1. Read the custom goal fields sent by the client
    room = goal_handle.request.room_name
    speed = goal_handle.request.patrol_speed
    
    node.get_logger().info(f'Starting Patrol Goal: Room="{room}" at Speed={speed} m/s')

    # Prepare your custom feedback structure objects
    feedback_msg = PatrolRoom.Feedback()
    
    # 2. Simulate a long-running patrol task over 5 steps
    start_time = time.time()
    for step in range(1, 6):
        # Update progress and text message dynamically
        progress = step * 20.0
        
        # Fill data slots exactly matching your custom .action file
        feedback_msg.percent_complete = progress
        if step < 3:
            feedback_msg.current_status = "Scanning area entrance..."
        else:
            feedback_msg.current_status = "Checking secure windows..."

        # 3. Publish the custom feedback back to the client live
        goal_handle.publish_feedback(feedback_msg)
        node.get_logger().info(f'Feedback Sent: {progress}% Complete.')
        
        time.sleep(2.0)  # Simulates 1 second passing per step

    # 4. Finalize the task, calculate values, and send the result package
    goal_handle.succeed()
    
    result = PatrolRoom.Result()
    result.success = True
    result.time_taken = float(time.time() - start_time)
    
    node.get_logger().info(f'Patrol Finished successfully in {result.time_taken:.2f}s!')
    return result

def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('patrol_action_server_node')

    # 5. Create the Action Server engine
    action_server = ActionServer(
        node,
        PatrolRoom,
        'patrol_room_service',
        lambda handle: execute_callback(handle, node)
    )

    node.get_logger().info('Custom Patrol Action Server is online and awaiting goals...')

    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass
    finally:
        action_server.destroy()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

